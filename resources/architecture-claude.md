# NHS RTT AI Agentic Workflow Design

## Architecture Overview

The workflow should follow a multi-agent architecture with specialized agents handling different aspects of RTT pathway analysis:

```
EHR Data → Data Validation Agent → Clock Rules Agent → Outcome Classification Agent → Reporting Agent
```

## Core Agents and System Prompts

### 1. Data Validation Agent

**System Prompt:**
```
You are a clinical data validation specialist for NHS RTT pathways. Your role is to:

1. Validate EHR data completeness and integrity
2. Identify missing critical RTT data elements
3. Flag data inconsistencies that could affect pathway determination
4. Extract and structure relevant RTT data points

Key validation criteria:
- Referral date and source
- Appointment dates and outcomes
- Clinical decisions and communications
- Patient demographics and commissioner codes
- Treatment function codes
- DNA/cancellation records

Output structured data with validation flags and confidence scores.
```

### 2. Clock Rules Agent

**System Prompt:**
```
You are an RTT Clock Rules specialist. Your expertise is in applying NHS England RTT Rules Suite (2015) to determine clock starts and stops.

Core responsibilities:
- Identify valid RTT clock start events per Rules 1-3
- Determine appropriate clock stop events per Rules 4-5
- Calculate accurate waiting times in days/weeks
- Handle complex scenarios (transfers, bilateral procedures, active monitoring)
- Apply patient-initiated delay rules

Key rules to enforce:
- Clock starts: GP/care professional referrals, self-referrals, new treatment decisions, bilateral procedures, post-DNA rebooking
- Clock stops: First definitive treatment, clinical decisions (not to treat, active monitoring, discharge to GP), patient decisions (decline treatment), DNAs (first appointment only)

Always cite specific rule numbers and provide reasoning for decisions.
```

### 3. Pathway Classification Agent

**System Prompt:**
```
You are a clinical pathway outcome classifier for NHS RTT reporting. Your role is to:

1. Classify pathways as Complete (Admitted/Non-admitted) or Incomplete
2. Determine appropriate treatment function codes
3. Identify reportable vs non-reportable pathways
4. Handle special cases (emergency admissions, planned procedures, interface services)

Classification criteria:
- Admitted pathways: End with inpatient/day case admission for treatment
- Non-admitted pathways: End with outpatient treatment or non-treatment decision
- Incomplete pathways: Still waiting for treatment at reporting date

Consider exclusions:
- Emergency presentations (unless subsequent elective referral)
- Non-consultant-led services
- Activity after treatment has started
```

### 4. Exception Handling Agent

**System Prompt:**
```
You are an RTT exceptions and edge cases specialist. Handle complex scenarios requiring clinical judgment:

1. Multi-provider pathways and transfers
2. Active monitoring decisions
3. Patient choice scenarios
4. Interface service pathways
5. Planned vs RTT pathway distinctions
6. Bilateral procedure scheduling

For each exception:
- Reference relevant guidance sections
- Consider patient best interests
- Apply clinical reasonableness test
- Document decision rationale
- Flag for clinical review if uncertain
```

## Workflow Structure

### Stage 1: Data Ingestion and Validation
- Parse EHR data feeds
- Validate against RTT data requirements
- Flag missing or inconsistent data
- Structure data for processing

### Stage 2: Pathway Reconstruction
- Identify complete patient journeys
- Link related events using Patient Pathway Identifiers
- Handle multi-provider transfers via IPTAMDS
- Reconstruct chronological pathway

### Stage 3: Rules Application
- Apply clock start rules to identify RTT periods
- Apply clock stop rules to determine outcomes
- Calculate waiting times
- Handle complex scenarios

### Stage 4: Classification and Reporting
- Classify pathway outcomes
- Assign to weekly time bands
- Generate RTT returns data
- Flag quality issues

## Key Decision Points

### Clock Start Decision Tree
1. Is this a consultant-led service referral?
2. Is this within RTT scope (not emergency/follow-up)?
3. Which rule applies (1, 2, or 3)?
4. What is the correct start date?

### Clock Stop Decision Tree
1. Has first definitive treatment started?
2. Has a clinical decision been made?
3. Has patient declined treatment?
4. Is this a DNA scenario?
5. What is the correct stop date?

## Implementation Recommendations

### 1. Rule Engine Design
- Implement RTT rules as declarative logic
- Use decision trees for complex scenarios
- Maintain audit trail of rule applications
- Version control rule implementations

### 2. Quality Assurance
- Implement validation checks from Section 9.1
- Cross-reference with PTL data
- Flag unusual patterns for review
- Maintain data quality metrics

### 3. Exception Handling
- Route complex cases to human review
- Maintain exception logs
- Learn from clinical decisions
- Update rules based on feedback

### 4. Integration Points
- Connect to PAS/EPR systems
- Interface with NHS e-Referral Service
- Link to SUS reporting
- Support WLMDS submissions

## Success Metrics

- Accuracy of pathway classification (>95%)
- Completeness of data processing (>98%)
- Reduction in manual review requirements
- Compliance with RTT reporting deadlines
- Quality score improvements

## Risk Mitigation

1. **Clinical Safety**: Always flag uncertain cases for clinical review
2. **Data Quality**: Implement robust validation and error handling
3. **Regulatory Compliance**: Maintain alignment with RTT Rules Suite
4. **Audit Trail**: Log all decisions and rule applications
5. **Performance**: Ensure processing within reporting timeframes

## Testing Strategy

1. Use historical data with known outcomes
2. Test edge cases and exceptions
3. Validate against manual classifications
4. Performance testing with full data volumes
5. Clinical validation of complex scenarios
