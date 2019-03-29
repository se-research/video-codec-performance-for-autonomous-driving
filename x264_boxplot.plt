set terminal pdf
set output "test.pdf"
set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot
# Setting the delimiter
set datafile separator ";"

set title "x264 Box plot"
set xtics ('1.0' 1, '1.2' 2, '1.3' 3)

# (x position):column
plot "res_1.txt" using (1.0):7:(2.0):10
