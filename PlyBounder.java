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
 *  CLASSPATH=/usr/share/java/commons-cli.jar:.  javac PlyBounder.java
 *
 * run:
 *  CLASSPATH=/usr/share/java/commons-cli.jar:.  java PlyBounder \
 *   plyPath=test_data \
 *   boundingBox="POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))" \
 *   outputPlyFile=alltogether.ply
 *
 */

import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.commons.cli.*;
import org.apache.commons.io.*;

public class PlyBounder {

  public static void main(String[] args) {

    // Get the commandline arguments
    Options options = new Options();
    // Available options
    options.addOption("plyPath", true, "directory containing input .ply files");
    options.addOption("boundingBox", true, "bounding box in WKT notation");
    options.addOption("outputPlyFile", true, "output file name");

    CommandLineParser parser = new DefaultParser();
    try {
      // parse the command line arguments
      // System.out.println(options);
      //System.out.println(args[0]);
      CommandLine line = parser.parse( options, args );
      if( line.hasOption( "plyPath" ) ) {
          // print the value of block-size
          System.out.println( "plyPath=" + line.getOptionValue( "plyPath" ) );
      }
      System.out.println( "plyPath=" + line.getOptionValue( "plyPath" ) );
    }
    catch( ParseException exp ) {
      System.err.println( "Error getting arguments: " + exp.getMessage() );
    }

    // input directory


    // Get list of files
    File dir = new File("./test_data");

		//System.out.println("Getting all files in " + dir.getCanonicalPath());
		List<File> files = (List<File>) FileUtils.listFiles(dir, new String[] { "ply","PLY"}, false);
		for (File file : files) {
      try{
        System.out.println("file=" + file.getCanonicalPath());
      }catch(IOException e){
        e.printStackTrace();
      }
		}

    // Loop through .ply files in directory
    //for file in files
      //ply-tool intersection inputfile "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))" setfile
    //done

    // Write new .ply file
    //ply-tool write setfile outputPlyFile

    // Done
    System.out.println("Done");
  }

}
