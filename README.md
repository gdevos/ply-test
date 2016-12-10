# ply-test

A few simple tests handling PLY polygon files   
http://paulbourke.net/dataformats/ply/   
http://www.dcs.ed.ac.uk/teaching/cs4/www/graphics/Web/ply.html   
It can show some info, work out intersections and combine multiple files into one.  

Uses Shapely, https://github.com/dranjan/python-plyfile and, in turn, NumPy   

## Usage:  

The Vagrantfile will show you the dependencies and set up.  
Let vagrant do all the work for you or do it yourself by copying what's in the "provision" part.    

Get vagrant at http://vagrantup.com  

Git clone this repo,  
cd into the directory and:  
```
vagrant up  # this might take some minutes to download and run  
```

Copy a directory with PLY files to work on into the work dir  
```
unzip test_data.zip
```

### Run the Java wrapper
```
vagrant ssh
cd /vagrant
javac PlyBounder.javac

java PlyBounder -plyPath test_data -boundingbox "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))" -outputPlyFile alltogether.ply

rm magweg.wkt

# OR
java PlyBounder -plyPath test_data -boundingbox "POLYGON ((-80 -10, 80 -80, 80 80, -80 80, -80 -10))" -outputPlyFile alltogether.ply

rm magweg.wkt
```

### Or run ply-tool.py directly
```
vagrant ssh
cd /vagrant
./ply-tool.py intersection test_data/house1.ply "POLYGON ((0 0, 0 80, 80 80, 80 0, 0 0))" outfile.WKT
./ply-tool.py write outfile.wkt outfile.ply

rm outfile.wkt
```

Between runs remove the magweg workfile to start fresh.  
