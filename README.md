# nfi_slot_manager
update free slots for freqtrade strategy nfi

### Slot Change Rules

**Basic Rules:**
- Base idle slot count: **3**
- Minimum total slots: **6**
- Maximum total slots: **20**

**De-risk Trade Impact:**
- Every **2 de-risk trades** reduce **1 idle slot**.
- For example, **3 de-risk trades** reduce **1 idle slot**.
- A minimum of **1 idle slot** must be maintained.

**Average Loss Impact:**
- When the average loss is between **-3% and -5%**: reduce **1 idle slot**.
- When the average loss is greater than **-5%**: reduce **2 idle slots**.
- A minimum of **1 idle slot** must be maintained.

**Maximum Loss Impact:**
- When the maximum loss is less than **-20%**: increase **2 idle slots**.
- When the maximum loss is less than **-10%**: increase **1 idle slot**.

---

### Example Scenarios

**Scenario 1: Normal Trading**

**Current open trades:** 5  
**De-risk trades:** 0  
**Average loss:** -1%  
**Maximum loss:** -5%

**Calculation Process:**
- **Base idle slots:** 3  
- No **De-risk impact**.  
- Average loss is minor: no impact.  
- Maximum loss is minor: no impact.  

**Final idle slots:** 3  
**Total slots:** 8 (5 + 3)  

---

**Scenario 2: With De-risk Trades**

**Current open trades:** 6  
**De-risk trades:** 4  
**Average loss:** -2%  
**Maximum loss:** -7%

**Calculation Process:**
- **Base idle slots:** 3  
- **De-risk impact:** -2 (4 de-risk trades reduce 2 slots).  
- Average loss is minor: no impact.  
- Maximum loss is minor: no impact.  

**Final idle slots:** 1  
**Total slots:** 7 (6 + 1)  

---

**Scenario 3: Severe Losses**

**Current open trades:** 4  
**De-risk trades:** 2  
**Average loss:** -6%  
**Maximum loss:** -22%

**Calculation Process:**
- **Base idle slots:** 3  
- **De-risk impact:** -1 (2 de-risk trades reduce 1 slot).  
- **Average loss > -5%:** -2.  
- **Maximum loss < -20%:** +2.  

**Final idle slots:** 2  
**Total slots:** 6 (4 + 2)

*/10 * * * * /home/devin/develop/nfi_slot_manager/cron.sh >> /home/devin/develop/nfi_slot_manager/cron.log 2>&1

