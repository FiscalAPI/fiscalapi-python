# FiscalAPI SDK - Payroll (CFDI Nomina) Requirements

This document describes the requirements for implementing payroll invoice (CFDI de Nomina) support in FiscalAPI SDKs. It is language-agnostic and focuses on the models, services, and functionality needed.

---

## Table of Contents

1. [Overview](#overview)
2. [New Models Required](#new-models-required)
3. [New Services Required](#new-services-required)
4. [Person Model Updates](#person-model-updates)
5. [Invoice Model Updates](#invoice-model-updates)
6. [Two Operation Modes](#two-operation-modes)
7. [Payroll Types Reference](#payroll-types-reference)
8. [API Endpoints](#api-endpoints)
9. [Field Mappings (JSON Aliases)](#field-mappings-json-aliases)
10. [Example Implementations](#example-implementations)

---

## Overview

Payroll invoices (CFDI de Nomina) in Mexico require:
- **Employer data** attached to the issuer (company paying wages)
- **Employee data** attached to the recipient (worker receiving wages)
- **Payroll complement** containing earnings, deductions, and other payment details

The SDK must support **13 different payroll types** and **two operation modes**:
1. **By Values** - All data sent inline with the invoice request
2. **By References** - Only person IDs sent; employee/employer data pre-configured via API

---

## New Models Required

### 1. EmployeeData

Data model for storing employee information as a sub-resource of Person.

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| employer_person_id | employerPersonId | string | ID of the employer person |
| employee_person_id | employeePersonId | string | ID of the employee person |
| social_security_number | socialSecurityNumber | string | NSS (Numero de Seguridad Social) |
| labor_relation_start_date | laborRelationStartDate | datetime | Employment start date |
| seniority | seniority | string | ISO 8601 duration (e.g., "P54W" = 54 weeks) |
| sat_contract_type_id | satContractTypeId | string | SAT contract type code |
| sat_unionized_status_id | satUnionizedStatusId | string | Unionized status code |
| sat_tax_regime_type_id | satTaxRegimeTypeId | string | Tax regime type code |
| sat_workday_type_id | satWorkdayTypeId | string | Workday type code |
| sat_job_risk_id | satJobRiskId | string | Job risk level code |
| sat_payment_periodicity_id | satPaymentPeriodicityId | string | Payment frequency code |
| employee_number | employeeNumber | string | Internal employee number |
| sat_bank_id | satBankId | string | Bank code |
| sat_payroll_state_id | satPayrollStateId | string | State code for payroll |
| department | department | string | Department name |
| position | position | string | Job position/title |
| bank_account | bankAccount | string | Bank account number |
| base_salary_for_contributions | baseSalaryForContributions | decimal | Base salary for social security |
| integrated_daily_salary | integratedDailySalary | decimal | Integrated daily salary |
| subcontractor_rfc | subcontractorRfc | string | RFC of subcontractor (if applicable) |
| time_percentage | timePercentage | decimal | Time percentage (for partial employment) |

### 2. EmployerData

Data model for storing employer information as a sub-resource of Person.

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| person_id | personId | string | ID of the employer person |
| employer_registration | employerRegistration | string | Registro Patronal (IMSS) |
| origin_employer_tin | originEmployerTin | string | RFC of origin employer |
| sat_fund_source_id | satFundSourceId | string | Fund source code |
| own_resource_amount | ownResourceAmount | decimal | Own resource amount |

### 3. InvoiceIssuerEmployerData

Employer data embedded in invoice issuer (for "by values" mode).

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| curp | curp | string | CURP of employer representative |
| employer_registration | employerRegistration | string | Registro Patronal |
| origin_employer_tin | originEmployerTin | string | RFC of origin employer |
| sat_fund_source_id | satFundSourceId | string | Fund source code |
| own_resource_amount | ownResourceAmount | decimal | Own resource amount |

### 4. InvoiceRecipientEmployeeData

Employee data embedded in invoice recipient (for "by values" mode).

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| curp | curp | string | CURP of employee |
| social_security_number | socialSecurityNumber | string | NSS |
| labor_relation_start_date | laborRelationStartDate | string | Start date (ISO format) |
| seniority | seniority | string | ISO 8601 duration |
| sat_contract_type_id | satContractTypeId | string | Contract type |
| sat_unionized_status_id | satUnionizedStatusId | string | Unionized status |
| sat_workday_type_id | satWorkdayTypeId | string | Workday type |
| sat_tax_regime_type_id | satTaxRegimeTypeId | string | Tax regime type |
| employee_number | employeeNumber | string | Employee number |
| department | department | string | Department |
| position | position | string | Position |
| sat_job_risk_id | satJobRiskId | string | Job risk code |
| sat_payment_periodicity_id | satPaymentPeriodicityId | string | Payment periodicity |
| sat_bank_id | satBankId | string | Bank code |
| bank_account | bankAccount | string | Bank account |
| base_salary_for_contributions | baseSalaryForContributions | decimal | Base salary |
| integrated_daily_salary | integratedDailySalary | decimal | Integrated salary |
| sat_payroll_state_id | satPayrollStateId | string | Payroll state |

### 5. Payroll Complement Models

#### PayrollComplement (main container)

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| version | version | string | Always "1.2" |
| payroll_type_code | payrollTypeCode | string | "O" (ordinary) or "E" (extraordinary) |
| payment_date | paymentDate | string | Payment date (ISO format) |
| initial_payment_date | initialPaymentDate | string | Period start date |
| final_payment_date | finalPaymentDate | string | Period end date |
| days_paid | daysPaid | decimal | Days paid in period |
| earnings | earnings | PayrollEarningsComplement | Earnings container |
| deductions | deductions | PayrollDeduction[] | List of deductions |
| disabilities | disabilities | PayrollDisability[] | List of disabilities |

#### PayrollEarningsComplement

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| earnings | earnings | PayrollEarning[] | List of earnings |
| other_payments | otherPayments | PayrollOtherPayment[] | Other payments (subsidies, etc.) |
| retirement | retirement | PayrollRetirement | Retirement/pension data |
| severance | severance | PayrollSeverance | Severance/indemnization data |

#### PayrollEarning

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| earning_type_code | earningTypeCode | string | SAT earning type code |
| code | code | string | Internal code |
| concept | concept | string | Description |
| taxed_amount | taxedAmount | decimal | Taxable amount |
| exempt_amount | exemptAmount | decimal | Exempt amount |
| stock_options | stockOptions | PayrollStockOptions | Stock options (if applicable) |
| overtime | overtime | PayrollOvertime[] | Overtime hours |

#### PayrollDeduction

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| deduction_type_code | deductionTypeCode | string | SAT deduction type code |
| code | code | string | Internal code |
| concept | concept | string | Description |
| amount | amount | decimal | Deduction amount |

#### PayrollOtherPayment

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| other_payment_type_code | otherPaymentTypeCode | string | SAT other payment type code |
| code | code | string | Internal code |
| concept | concept | string | Description |
| amount | amount | decimal | Payment amount |
| subsidy_caused | subsidyCaused | decimal | Employment subsidy caused |
| balance_compensation | balanceCompensation | PayrollBalanceCompensation | Balance compensation |

#### PayrollOvertime

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| days | days | int | Days with overtime |
| hours_type_code | hoursTypeCode | string | "01" (double) or "02" (triple) |
| extra_hours | extraHours | int | Number of extra hours |
| amount_paid | amountPaid | decimal | Amount paid |

#### PayrollDisability

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| disability_days | disabilityDays | int | Days of disability |
| disability_type_code | disabilityTypeCode | string | SAT disability type code |
| monetary_amount | monetaryAmount | decimal | Monetary amount |

#### PayrollRetirement

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| total_one_time | totalOneTime | decimal | One-time payment total |
| total_installments | totalInstallments | decimal | Installments total |
| daily_amount | dailyAmount | decimal | Daily amount |
| accumulable_income | accumulableIncome | decimal | Accumulable income |
| non_accumulable_income | nonAccumulableIncome | decimal | Non-accumulable income |

#### PayrollSeverance

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| total_paid | totalPaid | decimal | Total paid |
| years_of_service | yearsOfService | int | Years of service |
| last_monthly_salary | lastMonthlySalary | decimal | Last monthly salary |
| accumulable_income | accumulableIncome | decimal | Accumulable income |
| non_accumulable_income | nonAccumulableIncome | decimal | Non-accumulable income |

---

## New Services Required

### 1. EmployeeService

Sub-service of PeopleService for managing employee data.

```
Endpoint pattern: people/{personId}/employee
```

| Method | HTTP | Endpoint | Description |
|--------|------|----------|-------------|
| get_by_id(person_id) | GET | people/{personId}/employee | Get employee data |
| create(employee) | POST | people/{employeePersonId}/employee | Create employee data |
| update(employee) | PUT | people/{employeePersonId}/employee | Update employee data |
| delete(person_id) | DELETE | people/{personId}/employee | Delete employee data |

### 2. EmployerService

Sub-service of PeopleService for managing employer data.

```
Endpoint pattern: people/{personId}/employer
```

| Method | HTTP | Endpoint | Description |
|--------|------|----------|-------------|
| get_by_id(person_id) | GET | people/{personId}/employer | Get employer data |
| create(employer) | POST | people/{personId}/employer | Create employer data |
| update(employer) | PUT | people/{personId}/employer | Update employer data |
| delete(person_id) | DELETE | people/{personId}/employer | Delete employer data |

### 3. PeopleService Updates

Add employee and employer sub-services as properties:

```
client.people.employee  -> EmployeeService
client.people.employer  -> EmployerService
```

---

## Person Model Updates

Add the following field to the Person model:

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| curp | curp | string | CURP (Clave Unica de Registro de Poblacion) |

**Important**: For payroll invoices, the recipient (employee) must have:
- `curp` field populated
- `sat_tax_regime_id` = "605" (Sueldos y Salarios)
- `sat_cfdi_use_id` = "CN01" (Nomina)

---

## Invoice Model Updates

### InvoiceIssuer

Add field:

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| employer_data | employerData | InvoiceIssuerEmployerData | Employer data for payroll |

### InvoiceRecipient

Add field:

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| employee_data | employeeData | InvoiceRecipientEmployeeData | Employee data for payroll |

### InvoiceComplement

Add field:

| Field | JSON Alias | Type | Description |
|-------|------------|------|-------------|
| payroll | payroll | PayrollComplement | Payroll complement data |

---

## Two Operation Modes

### Mode 1: By Values

All employee/employer data is sent inline with the invoice request.

**Characteristics:**
- Self-contained request
- No prior setup required
- Larger payload size
- Employee data goes in `recipient.employee_data`
- Employer data goes in `issuer.employer_data`

**Example structure:**
```
Invoice {
  issuer: {
    tin: "EKU9003173C9",
    legal_name: "ESCUELA KEMPER URGATE",
    tax_regime_code: "601",
    employer_data: {
      employer_registration: "B5510768108",
      origin_employer_tin: "URE180429TM6"
    }
  },
  recipient: {
    tin: "XOJI740919U48",
    legal_name: "INGRID XODAR JIMENEZ",
    tax_regime_code: "605",
    cfdi_use_code: "CN01",
    employee_data: {
      curp: "XOJI850618MJCDNG09",
      social_security_number: "000000",
      seniority: "P54W",
      ...
    }
  },
  complement: {
    payroll: { ... }
  }
}
```

### Mode 2: By References

Only person IDs are sent; employee/employer data must be pre-configured.

**Characteristics:**
- Smaller payload
- Requires prior setup of employee/employer data via API
- Person must have CURP and tax regime configured
- Uses only `id` field in issuer/recipient

**Setup steps:**
1. Update person with CURP and tax regime (605 for employee, appropriate for employer)
2. Create EmployeeData via `client.people.employee.create()`
3. Create EmployerData via `client.people.employer.create()`

**Example structure:**
```
Invoice {
  issuer: {
    id: "2e7b988f-3a2a-4f67-86e9-3f931dd48581"
  },
  recipient: {
    id: "9367249f-f0ee-43f4-b771-da2fff3f185f"
  },
  complement: {
    payroll: { ... }
  }
}
```

---

## Payroll Types Reference

### 13 Standard Payroll Types

| # | Name | payroll_type_code | Key Characteristics |
|---|------|-------------------|---------------------|
| 1 | Ordinaria | O | Regular salary payment |
| 2 | Asimilados | O | Similar to salary (honorarios asimilados) |
| 3 | Bonos y Fondo de Ahorro | O | Bonuses and savings fund |
| 4 | Horas Extra | O | Overtime payment |
| 5 | Incapacidades | O | Disability/sick leave |
| 6 | SNCF | O | Federal government (SNCF) |
| 7 | Extraordinaria | E | Extraordinary payment |
| 8 | Separacion e Indemnizacion | E | Severance and indemnization |
| 9 | Jubilacion, Pension, Retiro | E | Retirement/pension |
| 10 | Sin Deducciones | O | Without deductions |
| 11 | Subsidio Causado | O | Employment subsidy adjustment |
| 12 | Viaticos | O | Travel expenses |
| 13 | Basica | O | Basic payroll |

### Common Invoice Fields for All Payroll Types

```
version_code: "4.0"
payment_method_code: "PUE"
currency_code: "MXN"
type_code: "N"
expedition_zip_code: <employer_zip_code>
export_code: "01"
```

### SAT Earning Type Codes (TipoPercepcion)

| Code | Description | Common Use |
|------|-------------|------------|
| 001 | Sueldos, Salarios Rayas y Jornales | Regular salary |
| 002 | Gratificación Anual (Aguinaldo) | Christmas bonus |
| 003 | Participación de los Trabajadores en las Utilidades PTU | Profit sharing |
| 019 | Horas extra | Overtime |
| 022 | Prima vacacional | Vacation bonus |
| 023 | Pagos por separación | Severance pay |
| 025 | Indemnizaciones | Indemnization |
| 028 | Comisiones | Commissions |
| 029 | Vales de despensa | Food vouchers |
| 039 | Jubilaciones, pensiones o haberes de retiro | Retirement |
| 044 | Jubilaciones, pensiones o haberes de retiro parcial | Partial retirement |
| 045 | Ingresos en acciones | Stock income |
| 046 | Ingresos asimilados a salarios | Income similar to salary |
| 047 | Alimentación | Food |
| 050 | Viáticos | Travel expenses |

### SAT Deduction Type Codes (TipoDeduccion)

| Code | Description | Common Use |
|------|-------------|------------|
| 001 | Seguridad social | Social security |
| 002 | ISR | Income tax |
| 003 | Aportaciones a retiro | Retirement contributions |
| 004 | Otros | Other deductions |
| 006 | Descuento por incapacidad | Disability discount |
| 010 | Pensión alimenticia | Alimony |
| 020 | Fondo de ahorro | Savings fund |
| 081 | Ajuste en viáticos | Travel expense adjustment |
| 107 | Ajuste al Subsidio Causado | Subsidy adjustment |

### SAT Other Payment Type Codes (TipoOtroPago)

| Code | Description |
|------|-------------|
| 001 | Reintegro de ISR pagado en exceso |
| 002 | Subsidio para el empleo |
| 003 | Viáticos |
| 004 | Aplicación de saldo a favor por compensación anual |
| 007 | ISR ajustado por subsidio |

---

## API Endpoints

### Employee Endpoints

```
GET    /api/{version}/people/{personId}/employee
POST   /api/{version}/people/{personId}/employee
PUT    /api/{version}/people/{personId}/employee
DELETE /api/{version}/people/{personId}/employee
```

### Employer Endpoints

```
GET    /api/{version}/people/{personId}/employer
POST   /api/{version}/people/{personId}/employer
PUT    /api/{version}/people/{personId}/employer
DELETE /api/{version}/people/{personId}/employer
```

### Invoice Endpoints

Payroll invoices use the standard invoice endpoint:

```
POST /api/{version}/invoices
```

With `type_code: "N"` for payroll invoices.

---

## Field Mappings (JSON Aliases)

All models must serialize using camelCase JSON aliases when communicating with the API.

**Serialization rules:**
- Use camelCase for JSON property names
- Exclude null/None values from JSON
- Decimal values should serialize as strings
- Dates should serialize as ISO 8601 strings

---

## Example Implementations

### Example 1: Create Payroll Invoice (By Values)

```
// Pseudocode - adapt to target language

invoice = Invoice(
  version_code: "4.0",
  series: "F",
  date: "2026-01-25T10:00:00",
  payment_method_code: "PUE",
  currency_code: "MXN",
  type_code: "N",
  expedition_zip_code: "20000",
  export_code: "01",

  issuer: InvoiceIssuer(
    tin: "EKU9003173C9",
    legal_name: "ESCUELA KEMPER URGATE",
    tax_regime_code: "601",
    employer_data: InvoiceIssuerEmployerData(
      employer_registration: "B5510768108",
      origin_employer_tin: "URE180429TM6"
    )
  ),

  recipient: InvoiceRecipient(
    tin: "XOJI740919U48",
    legal_name: "INGRID XODAR JIMENEZ",
    zip_code: "76028",
    tax_regime_code: "605",
    cfdi_use_code: "CN01",
    employee_data: InvoiceRecipientEmployeeData(
      curp: "XOJI850618MJCDNG09",
      social_security_number: "000000",
      labor_relation_start_date: "2015-01-01",
      seniority: "P437W",
      sat_contract_type_id: "01",
      sat_workday_type_id: "01",
      sat_tax_regime_type_id: "02",
      employee_number: "120",
      department: "Desarrollo",
      position: "Ingeniero de Software",
      sat_job_risk_id: "1",
      sat_payment_periodicity_id: "04",
      sat_bank_id: "002",
      bank_account: "1111111111",
      base_salary_for_contributions: 490.22,
      integrated_daily_salary: 146.47,
      sat_payroll_state_id: "JAL"
    )
  ),

  complement: InvoiceComplement(
    payroll: PayrollComplement(
      version: "1.2",
      payroll_type_code: "O",
      payment_date: "2023-05-24",
      initial_payment_date: "2023-05-09",
      final_payment_date: "2023-05-24",
      days_paid: 15,
      earnings: PayrollEarningsComplement(
        earnings: [
          PayrollEarning(
            earning_type_code: "001",
            code: "00500",
            concept: "Sueldos, Salarios Rayas y Jornales",
            taxed_amount: 2808.80,
            exempt_amount: 2191.20
          )
        ]
      ),
      deductions: [
        PayrollDeduction(
          deduction_type_code: "001",
          code: "00301",
          concept: "Seguridad Social",
          amount: 200.00
        ),
        PayrollDeduction(
          deduction_type_code: "002",
          code: "00302",
          concept: "ISR",
          amount: 100.00
        )
      ]
    )
  )
)

response = client.invoices.create(invoice)
```

### Example 2: Setup for By References Mode

```
// Step 1: Update person with CURP and tax regime
employee_person = Person(
  id: "9367249f-f0ee-43f4-b771-da2fff3f185f",
  curp: "XOJI850618MJCDNG09",
  sat_tax_regime_id: "605",
  sat_cfdi_use_id: "CN01"
)
client.people.update(employee_person)

// Step 2: Create employee data
employee_data = EmployeeData(
  employer_person_id: "2e7b988f-3a2a-4f67-86e9-3f931dd48581",
  employee_person_id: "9367249f-f0ee-43f4-b771-da2fff3f185f",
  social_security_number: "000000",
  labor_relation_start_date: datetime(2015, 1, 1),
  seniority: "P437W",
  sat_contract_type_id: "01",
  sat_workday_type_id: "01",
  sat_tax_regime_type_id: "02",
  employee_number: "120",
  department: "Desarrollo",
  position: "Ingeniero de Software",
  sat_job_risk_id: "1",
  sat_payment_periodicity_id: "04",
  sat_bank_id: "002",
  bank_account: "1111111111",
  integrated_daily_salary: 146.47,
  sat_payroll_state_id: "JAL"
)
client.people.employee.create(employee_data)

// Step 3: Create employer data
employer_data = EmployerData(
  person_id: "2e7b988f-3a2a-4f67-86e9-3f931dd48581",
  employer_registration: "B5510768108",
  origin_employer_tin: "URE180429TM6"
)
client.people.employer.create(employer_data)
```

### Example 3: Create Payroll Invoice (By References)

```
invoice = Invoice(
  version_code: "4.0",
  series: "F",
  date: "2026-01-25T10:00:00",
  payment_method_code: "PUE",
  currency_code: "MXN",
  type_code: "N",
  expedition_zip_code: "20000",
  export_code: "01",

  // Only IDs - data comes from pre-configured employee/employer
  issuer: InvoiceIssuer(
    id: "2e7b988f-3a2a-4f67-86e9-3f931dd48581"
  ),
  recipient: InvoiceRecipient(
    id: "9367249f-f0ee-43f4-b771-da2fff3f185f"
  ),

  complement: InvoiceComplement(
    payroll: PayrollComplement(
      // Same payroll data as by-values mode
      version: "1.2",
      payroll_type_code: "O",
      payment_date: "2023-05-24",
      initial_payment_date: "2023-05-09",
      final_payment_date: "2023-05-24",
      days_paid: 15,
      earnings: PayrollEarningsComplement(
        earnings: [
          PayrollEarning(
            earning_type_code: "001",
            code: "00500",
            concept: "Sueldos, Salarios Rayas y Jornales",
            taxed_amount: 2808.80,
            exempt_amount: 2191.20
          )
        ]
      ),
      deductions: [
        PayrollDeduction(
          deduction_type_code: "001",
          code: "00301",
          concept: "Seguridad Social",
          amount: 200.00
        ),
        PayrollDeduction(
          deduction_type_code: "002",
          code: "00302",
          concept: "ISR",
          amount: 100.00
        )
      ]
    )
  )
)

response = client.invoices.create(invoice)
```

---

## Implementation Checklist

- [ ] Add `curp` field to Person model
- [ ] Create EmployeeData model
- [ ] Create EmployerData model
- [ ] Create InvoiceIssuerEmployerData model
- [ ] Create InvoiceRecipientEmployeeData model
- [ ] Create PayrollComplement and all sub-models
- [ ] Add employer_data to InvoiceIssuer model
- [ ] Add employee_data to InvoiceRecipient model
- [ ] Add payroll to InvoiceComplement model
- [ ] Create EmployeeService with CRUD operations
- [ ] Create EmployerService with CRUD operations
- [ ] Add employee and employer properties to PeopleService
- [ ] Create examples for all 13 payroll types (by values)
- [ ] Create examples for all 13 payroll types (by references)
- [ ] Create setup data methods for by-references mode
- [ ] Test all payroll types successfully

---

## Notes

1. **Seniority format**: Use ISO 8601 duration format (e.g., "P437W" for 437 weeks)
2. **Tax regime for employees**: Always "605" (Sueldos y Salarios)
3. **CFDI use for payroll**: Always "CN01" (Nomina)
4. **Invoice type**: Always "N" for payroll invoices
5. **Payment method**: Typically "PUE" (Pago en Una sola Exhibicion)
6. **Payroll complement version**: Always "1.2"
