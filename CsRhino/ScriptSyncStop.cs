using System;
using System.Collections.Generic;

using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;

namespace ScriptSync
{
    public class ScriptSyncStop : Command
    {
        public ScriptSyncStop()
        {
            Instance = this;
        }

        public static ScriptSyncStop Instance { get; private set; }

        public override string EnglishName => "ScriptSyncStop";

        protected override Rhino.Commands.Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // start a local server
            if ( !ScriptSyncStart.Instance.IsRunning )
            {
                RhinoApp.WriteLine("ScriptSync not running");
                return Rhino.Commands.Result.Success;
            }
            Stop();
            return Rhino.Commands.Result.Success;
        }

        /// <summary>
        /// It is called on a thread to run the server and listen for incoming paths to run.
        /// </summary>
        private void Stop()
        {
            ScriptSyncStart.Instance.IsRunning = false;
            using (TcpClient client = new TcpClient())
            {
                try
                {
                    client.Connect(IPAddress.Parse(ScriptSyncStart.Instance.Ip), ScriptSyncStart.Instance.Port);
                }
                catch (Exception e)
                {
                    RhinoApp.WriteLine("Error: " + e.Message);
                    return;
                }
            }
        }
    }
}
