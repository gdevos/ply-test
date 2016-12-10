/* PlyBounder
 * (c) Gerard de Vos, ASL licensed
 *
 *PlyBounder reads .ply files, creates a matching set based
 * on a boundingBox and writes this set to a new .ply file
 *
 * ArgumentParser
 * --plyPath=inputdirectory
 * --boundingBox=WKTstring
 * --outputPlyFile=outputfilename
 *
 * build:
 *  CLASSPATH=/usr/share/java/commons-cli.jar:/usr/share/java/commons-io.jar:. \
 *   javac PlyBounder.java
 *
 * run:
 * CLASSPATH=/usr/share/java/commons-cli.jar:/usr/share/java/commons-io.jar:.    java PlyBounder
 * -plyPath test_data
 * -boundingbox "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"
 * -outputPlyFile alltogether.ply
 *
 */

import java.io.*; // deprecated?
import java.util.List;

import org.apache.commons.cli.*;
import org.apache.commons.io.*;

public class PlyBounder {

  public static void main(String[] args) {

    // Get the commandline arguments
    Options options = new Options();
    // Available options
    Option plyPath = OptionBuilder.withArgName( "dir" )
                                .hasArg()
                                .withDescription( "directory containing input .ply files" )
                                .create( "plyPath" );
    Option boundingbox = OptionBuilder.withArgName( "string" )
                                .hasArg()
                                .withDescription( "bounding box in WKT notation" )
                                .create( "boundingbox" );
    Option outputPlyFile = OptionBuilder.withArgName( "file" )
                                .hasArg()
                                .withDescription( "output PLY file name" )
                                .create( "outputPlyFile" );
    options.addOption( plyPath );
    options.addOption( boundingbox );
    options.addOption( outputPlyFile );

    String plydir = ".";
    String boundingboxstr = "";
    String outputfilename = "";

    CommandLineParser parser = new DefaultParser();
    try {
      // parse the command line arguments
      CommandLine line = parser.parse( options, args );

      boundingboxstr = line.getOptionValue( "boundingbox" );
      outputfilename = line.getOptionValue( "outputPlyFile" );

      if( line.hasOption( "plyPath" ) ) {
        // print the value of block-size
        plydir = line.getOptionValue( "plyPath" );
        System.out.println( "Using plyPath=" + plydir );
      } else {
        HelpFormatter formatter = new HelpFormatter();
        formatter.printHelp( "PlyBounder", options );
      }
      //System.out.println( "plyPath=" + line.getOptionValue( "plyPath" ) );
    }
    catch( ParseException exp ) {
      System.err.println( "Error getting arguments: " + exp.getMessage() );
    }

    // input directory
    // Get list of files
    File dir = new File( plydir );

		//System.out.println("Getting all files in " + dir.getCanonicalPath());
		List<File> files = (List<File>) FileUtils.listFiles(dir, new String[] { "ply","PLY"}, false);
		for (File file : files) {
      try{
        System.out.println("file=" + file.getCanonicalPath());
      }catch(IOException e){
        e.printStackTrace();
      }
		}

    String sometempfile = "magweg.wkt";
    String s = null;

    // Loop through .ply files in directory
    for (File file : files) {
      try{
        String cmdl[] = { "./ply-tool.py", "intersection", file.getCanonicalPath(), boundingboxstr, sometempfile };
        //System.out.println("Running: " + Arrays.toString(cmdl));
        Process p = Runtime.getRuntime().exec(cmdl);

        BufferedReader stdInput = new BufferedReader(new
        InputStreamReader(p.getInputStream()));

        BufferedReader stdError = new BufferedReader(new
        InputStreamReader(p.getErrorStream()));

        // read the output from the command
        System.out.println("cmdout:\n");
        while ((s = stdInput.readLine()) != null) {
          System.out.println(s);
        }

        // read any errors from the attempted command
        System.out.println("cmderr:\n");
        while ((s = stdError.readLine()) != null) {
          System.out.println(s);
        }
      }catch(IOException e){
        e.printStackTrace();
      }
		}

    // Write new .ply file
    //ply-tool write setfile outputPlyFile
    try{
      String cmdl = "./ply-tool.py write " + sometempfile + " " + outputfilename ;
      System.out.println("Running: " + cmdl);
      Process p = Runtime.getRuntime().exec(cmdl);

      BufferedReader stdInput = new BufferedReader(new
      InputStreamReader(p.getInputStream()));

      BufferedReader stdError = new BufferedReader(new
      InputStreamReader(p.getErrorStream()));

      // read the output from the command
      System.out.println("cmdout:\n");
      while ((s = stdInput.readLine()) != null) {
        System.out.println(s);
      }

      // read any errors from the attempted command
      System.out.println("cmderr:\n");
      while ((s = stdError.readLine()) != null) {
        System.out.println(s);
      }
    }catch(IOException e){
      e.printStackTrace();
    }

    // Done
    System.out.println("Done");
  }

}
