# Dynatrace-SLO-Report
- Automatically generates SLO reports (Pandas/Excel) from your Dynatrace environments.

## Prerequisites
- Python 3.x (or lastest). [Download](https://www.python.org/downloads/)
- Dynatrace API Token (*Settings > Integration > Dynatrace API*)
 
## How to use it?
1. Configure the file `config.ini`:
    - [DATES]
        - Specify the desired time range.
    - [TENANTS]   
        - Specify all the tenants to extract the data from. i.e.:
            ```
            tenant1 = https://abc12345.live.dynatrace.com <token>
            #tenant2 = https://abc22345.live.dynatrace.com <token>
            ...
            tenant3 = https://abc32345.live.dynatrace.com <token>
            ```        
        - Use comments to avoid getting the data from a specific tenant  
2. `cd <python file location>`
3. Execute: ```python usage-calculation.py```
    - Note: Make sure to have installed python packages: `pip install <package-name>`
4. Results will be stored in different folders (per enviroment) and sheets (per day).
