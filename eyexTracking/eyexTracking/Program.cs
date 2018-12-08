using System;
using System.Diagnostics;
using System.IO;
using Tobii.EyeX;
using Tobii.Interaction;

namespace eyexTracking
{
    class Program
    {
        
        static void Main(string[] args)
        {
            FileStream fst;
            StreamWriter writer;
            Program p = new Program();
            
         //   p.eyeTracker_EyeXHost();
            Console.WriteLine("Listening for gaze data, press any key to exit...");
            Console.WriteLine("2nd line");
            //   var i = 0;
            //   while (true) {
            //       Console.WriteLine("{0}",i+1);
            //   }
            fst = new FileStream("./data3.txt",FileMode.OpenOrCreate, FileAccess.Write);
            writer = new StreamWriter(fst);
            
            p.eyeTracker_Host(writer);
            Console.In.Read();
           // system("pause");
        }

        //-------------------------EyeXHost---------------------------
        public void eyeTracker_EyeXHost() {
            var eyeXHost = new EyeXFramework.EyeXHost();
            var gazePointDataStream1 = eyeXHost.CreateGazePointDataStream(Tobii.EyeX.Framework.GazePointDataMode.LightlyFiltered);
            eyeXHost.Start();
            gazePointDataStream1.Next += (s, e) => Console.WriteLine("Gaze point at ({0:0.0}, {1:0.0}) @{2:0}", e.X, e.Y, e.Timestamp);
        }

        //------------------------Host-------------------------------
        public void eyeTracker_Host(StreamWriter writer) {
            var host = new Host();
         //   var headStream = host.Streams.CreateHeadPoseStream(true);

         //   headStream.Next += (s, e) => Console.WriteLine("Head pose : X: {0}  Y: {1}",e.Data.HeadPosition.X,e.Data.HeadPosition.Y, e.Data.HeadPosition.Z);
        
            

         //   var eyePositionStream = host.Streams.CreateEyePositionStream(true);
            var gazePointDataStream = host.Streams.CreateGazePointDataStream(Tobii.Interaction.Framework.GazePointDataMode.LightlyFiltered);
            //   gazePointDataStream.Next += (s, e) => Console.WriteLine("X: {0}, y: {1}, t: {2}, engineT: {3}", e.Data.X, e.Data.Y, e.Data.Timestamp, e.Data.EngineTimestamp);
            //
            //   eyePositionStream.Next += (s, e) => Console.WriteLine("Eye position: \n Left Eye : X:{0}, Y:{1}, Z:{2}, \n " +
            //       "Right Eye : X: {3}, Y: {4}, Z: {5}, timestamp : {6}, engineT: {7},{8},{9}",
            //       e.Data.LeftEye.X, e.Data.LeftEye.Y, e.Data.LeftEye.Z,
            //       e.Data.RightEye.X, e.Data.RightEye.Y, e.Data.RightEye.Z, e.Data.Timestamp, e.Data.EngineTimestamp, e.Data.LeftEyeNormalized.X,e.Data.LeftEyeNormalized.Y);

           // GazePointData gazeD = null;
            Console.WriteLine("Hello");
           
                gazePointDataStream.Next += (s, e) => Console.WriteLine("g:{0}|{1}|{2}|", e.Data.X, e.Data.Y, e.Data.EngineTimestamp);
            //    Console.WriteLine("g:{0}|{1}|{2}|", gazeD.X, gazeD.Y, gazeD.EngineTimestamp);
                
           
           
            Console.WriteLine("Hello again");
            //     eyePositionStream.Next += (s, e) => Console.WriteLine("e:{0}|{1}|{2}|{3}|{4}|{5}|{6}",
            //            e.Data.LeftEye.X, e.Data.LeftEye.Y, e.Data.LeftEye.Z,
            //            e.Data.RightEye.X, e.Data.RightEye.Y, e.Data.RightEye.Z, e.Data.EngineTimestamp);

            //    gazePointDataStream.Next += (s, e) => writer.WriteLine("{0}|{1}|{2}|", e.Data.X, e.Data.Y, e.Data.EngineTimestamp);
            //    eyePositionStream.Next += (s, e) => writer.Write("{0}|{1}|{2}|{3}|{4}|{5}|{6}",
            //           e.Data.LeftEye.X, e.Data.LeftEye.Y, e.Data.LeftEye.Z,
            //           e.Data.RightEye.X, e.Data.RightEye.Y, e.Data.RightEye.Z, e.Data.EngineTimestamp);
            //   gazePointDataStream.GazePoint((gazePointX, gazePointY, t) => Console.WriteLine("X: {0} Y: {1} t: {2}", gazePointX, gazePointY, t));
        }
    }
}
