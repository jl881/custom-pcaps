Using functions written by RPGillespie on codeproject.com -- thank you!  
https://www.codeproject.com/Tips/612847/Generate-a-quick-and-easy-custom-pcap-file-using-P

Happy packeting!

## Usage

`python custom-pcaps.py <list of timestamps (us)> <packet length> <src mac> <outputfile>`  
  
### Note 1
   
`<list of timestamps (us)>` can either be:  
-in the format `[x,y,z]`  
eg `python custom_512.py [0,2,4] 1024 cccccccccccc meow.pcap`  
-or a filename containing a list `[x,y,z]`  
eg `python custom_512.py tsfile.txt 1024 cccccccccccc meow.pcap`

### Note 2
no punctuation in the src mac. Default dest mac is `ffffffffffff`, but can be easily changed in the script.
