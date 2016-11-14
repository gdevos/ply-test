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
 */

import org.apache.commons.cli.*;

public class PlyBounder {

  public static void GetArguments(String[] args) {
    Options options = new Options();
    // Available options
    options.addOption("plyPath", true, "directory containing input .ply files");
    options.addOption("boundingBox", true, "bounding box in WKT notation");
    options.addOption("outputPlyFile", true, "output file name");

    CommandLineParser parser = new DefaultParser();
    try {
      // parse the command line arguments
      System.out.println(options);
      System.out.println(args[0]);
      CommandLine line = parser.parse( options, args );
    }
    catch( ParseException exp ) {
      System.err.println( "Error getting arguments: " + exp.getMessage() );
    }
  }

  public static void main(String[] args) {
    // Get the commandline arguments
    GetArguments(args);


    // Get list of files

    // Loop through .ply files in directory
    //for file in files
      //ply-tool intersection inputfile boundingBox setfile
    //done

    // Write new .ply file
    //ply-tool write setfile outputPlyFile

    // Done
    System.out.println("Done");
  }

}
