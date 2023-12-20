using System;

CsVersion.Main();

class CsVersion
{
    static public void Main()
    {
        Console.WriteLine("C# Runtime: " + Environment.Version.ToString());
        Console.WriteLine("platform: " + Environment.OSVersion.ToString());
    }
}
