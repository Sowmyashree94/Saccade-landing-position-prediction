using System;
using Tobii.Interaction;
using System.Timers;

namespace eyeX_tracker
{
    class Program
    {
        static void Main(string[] args)
        {
            Program p = new Program();
            var host = new Host();
            p.eyeTracker_Host(host);
            Console.In.Read();
        }
        //------------------------Host-------------------------------
        public void eyeTracker_Host(Host host)
        {

            System.Timers.Timer t = new System.Timers.Timer(60000);
            t.Elapsed += (s, e) => timerStop(host, e, t);
            t.Enabled = true;
            var gazePointDataStream = host.Streams.CreateGazePointDataStream(Tobii.Interaction.Framework.GazePointDataMode.LightlyFiltered);
            GazePointDataStream gazePointDataStream1 = gazePointDataStream;
            gazePointDataStream1.Next += (s, e) => Console.WriteLine("{0} {1}", e.Data.X, e.Data.Y);

        }
        public void timerStop(Host host, ElapsedEventArgs e, System.Timers.Timer t)
        {
            Console.WriteLine("Ran for : " + e.SignalTime);
            host.DisableConnection();
            t.Enabled = false;
            Environment.Exit(0);
        }
    }
}
