using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using Rhino.PlugIns;

// Plug-in Description Attributes - all of these are optional.
// These will show in Rhino's option dialog, in the tab Plug-ins.
[assembly: PlugInDescription(DescriptionType.Address, "")]
[assembly: PlugInDescription(DescriptionType.Country, "Switzerland")]
[assembly: PlugInDescription(DescriptionType.Email, "andrea.settimi@epfl.ch")]
[assembly: PlugInDescription(DescriptionType.Phone, "")]
[assembly: PlugInDescription(DescriptionType.Fax, "")]
[assembly: PlugInDescription(DescriptionType.Organization, "IBOIS, EPFL")]
[assembly: PlugInDescription(DescriptionType.UpdateUrl, "https://github.com/ibois-epfl/script-sync")]
[assembly: PlugInDescription(DescriptionType.WebSite, "https://github.com/ibois-epfl/script-sync")]

// Icons should be Windows .ico files and contain 32-bit images in the following sizes: 16, 24, 32, 48, and 256.
[assembly: PlugInDescription(DescriptionType.Icon, "ScriptSync.EmbeddedResources.logo.scriptsync_48.ico")]

// The following GUID is for the ID of the typelib if this project is exposed to COM
// This will also be the Guid of the Rhino plug-in
[assembly: Guid("41B699D3-5B19-43FC-BD2A-AAD30B88ACC7")] 
