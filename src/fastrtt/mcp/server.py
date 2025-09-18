import json
import os
from datetime import datetime
from io import BytesIO
from typing import Annotated

import pandas as pd
import pymssql
from markitdown import MarkItDown
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

# # Default host and port values, can be overridden via environment variables
# NotImplemented
# host = os.environ.get("MCP_HOST", "localhost")
# port = int(os.environ.get("MCP_PORT", "8000"))

mcp = FastMCP(name="OMOP MCP Server")

# Get database connection using environment variables

db_conn_params = dict(
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"],
)


def pdf2text(bytes_data: bytes) -> str:
    """Convert PDF bytes data to text using MarkItDown."""
    md = MarkItDown()
    text = md.convert(BytesIO(bytes_data))
    print(text)
    return text


@mcp.tool(
    name="Get_Notes_List",
    description="Get a list of notes from the FastRTT database.",
)
def get_notes_list(
    person_id: Annotated[str, "The ID of the patient to retrieve notes for."],
    start_date: Annotated[
        str, "The start date for the notes to retrieve. Formatted as YYYY-MM-DD"
    ],
    end_date: Annotated[
        str, "The end date for the notes to retrieve. Formatted as YYYY-MM-DD"
    ] = datetime.now().strftime("%Y-%m-%d"),
) -> CallToolResult:
    """This function retrieves a list of notes for a specific patient between a date interval.

    Args:
        person_id:  The ID of the patient to retrieve notes for.
        start_date: The start date for the notes to retrieve. Formatted as YYYY-MM-DD.
                    This is typically the clock start date although a prior or later date can be used for more or less context respectively.
        end_date:   The end date for the notes to retrieve.
                    This typically today altough a past date can be used where there are a very large number of notes.

    Returns:
        Date ordered JSON array with the following keys:
            note_date
            note_text
            department
            note_type

    """

    sql = """
SELECT 
    note_id,
    person_id,
    note_date,
    note_text,
    department,
    note_source_value as note_type
FROM FastRTT.fastrtt.stg__note
WHERE
    person_id = %s
    and note_date between %s and %s;
"""

    try:
        with pymssql.connect(**db_conn_params) as conn:
            df = pd.read_sql(sql, conn, params=(person_id, start_date, end_date))

        df["note_text"] = df["note_text"].apply(pdf2text)

        result = df.to_json(orient="records")

        return CallToolResult(
            content=[
                TextContent(type="text", text=result),
            ]
        )
    except Exception as e:
        return CallToolResult(
            isError=True,
            content=[
                TextContent(
                    type="text",
                    text=f"Failed to retrieve notes {str(e)}",
                )
            ],
        )


def main():
    """Main function to run the MCP server."""

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
