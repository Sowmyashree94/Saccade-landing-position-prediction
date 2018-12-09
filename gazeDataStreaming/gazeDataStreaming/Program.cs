using System;
using System.Timers;
using Tobii.Interaction;
namespace eyexTracking
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
            Console.WriteLine("Hello");
            GazePointDataStream gazePointDataStream1 = gazePointDataStream;
            //gazePointDataStream1.GazePoint((x, y, ts) => Console.WriteLine("Timestamp: {0}\t X: {1} Y:{2}", ts, x, y));
            gazePointDataStream1.Next += (s, e) => Console.WriteLine("{0}|{1}|{2}", e.Data.X, e.Data.Y, e.Data.Timestamp);

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