library(Rglpk)

a <- numeric(0)
for (i in 0:29){
  print(i)
  filename = sprintf("~/Desktop/Reading/Optimization Model Files/ReadingPlan%d.mps",i)
  m <- Rglpk_read_file(filename, type="MPS_free")
  t<-system.time(Rglpk_solve_LP(m$objective, m$constraints[[1]], m$constraints[[2]],
                                m$constraints[[3]], m$bounds, m$types, max=TRUE))
  print(as.numeric(t[3]))
  a <- append(a,as.numeric(t[3]))
}
a
write.csv(a, "ROutput.csv")



library(lpSolve)
library(lpSolveAPI)
c <- numeric(0)
for (i in 0:29){
  print(i)
  filename = sprintf("~/Desktop/Reading/Optimization Model Files/ReadingPlan%d.mps",i)
  m <- read.lp(filename, type="freemps", verbose="normal")
  lp.control(m, sense='max')
  lp.control(m, verbose='neutral') #mask messages
  t<-system.time(solve.lpExtPtr(m))
  print(as.numeric(t[3]))
  c <- append(c,as.numeric(t[3]))
}
c
write.csv(c, "ROutputLPSolveAPI-2.csv")