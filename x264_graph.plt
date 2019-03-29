# Setting output type
set terminal pdf
# Output file name
set output "graph_collection.pdf"
# Graph title
set title "X264 Data"

set xlabel "SSIM"
set ylabel "Value"

#
# A plot using the filename.txt using the first and second column,
# with data as a line called Something. 
#
plot "filename.txt" using 1:2 with lines title "Something"
