def execute_powershell(script):
    assembly_path = r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Management.Automation\v4.0_3.0.0.0__31bf3856ad364e35\System.Management.Automation.dll"
    try:
        # Load the .NET assemblies
        clr.AddReference(assembly_path)
        from System.Management.Automation import PowerShell
            
        # Create a PowerShell instance
        ps_instance = PowerShell.Create()
        
        # Add the script to the instance
        ps_instance.AddScript(script)
            
        # Execute the script
        results = ps_instance.Invoke()
            
        # Collect the results
        output = []
        for result in results:
            output.append(str(result))
            
        return "\n".join(output)

             
    except Exception as e:
        return f"Error executing PowerShell script: {str(e)}"
        