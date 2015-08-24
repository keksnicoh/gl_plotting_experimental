

c HW #6  Computing PI using Monte Carlo

        program calcpi

        implicit real (a-h, o-z)
        implicit integer (i-n)

        integer :: counti, countf, count_rate
		real    :: dt
		call system_clock(counti,count_rate)

        write(*,*) 'Choose n: '
        read(*,*) n 
       
        id = -5
 
        nhit = 0 

        do 50 i=1, n
           x = ran1(id)   
           y = ran1(id)  

c Calculate radius
c  NOTE: no need to waste computation time on square root
c        since we are comparing to 1.
c
           r = x**2.0 + y**2.0

           if (r.le. 1.0) then 
              nhit=nhit+1 
           endif

  50    continue

* Find the ratio of points in the circle to the total points used

        write(*,*) 
        write(*,*) n, nhit
        pi = 4.0 * (real(nhit)/real(n))
c
c Calcualte Actual Value of Pi and % Error
c
        pi_act = acos(-1.0) 

        rerror = abs((pi_act - pi)/ pi_act)

        call system_clock(countf)
		dt=REAL(countf-counti)/REAL(count_rate)
       
        write(*,100) n, pi, pi_act, rerror, dt
 100    format(2x, i8, f15.8, f15.8, f15.8, f15.8)
c
        stop
        end
         

C return a uniform random deviate between 0.0 and 1.0. 
C Call with negative idum to initiate.
C
      real FUNCTION ran1(idum)
      INTEGER idum,IA,IM,IQ,IR,NTAB,NDIV
      real AM,EPS,RNMX
      PARAMETER (IA=16807,IM=2147483647,AM=1./IM,IQ=127773,IR=2836,
     *NTAB=32,NDIV=1+(IM-1)/NTAB,EPS=1.2e-7,RNMX=1.-EPS)
      INTEGER j,k,iv(NTAB),iy
      SAVE iv,iy
      DATA iv /NTAB*0/, iy /0/
      if (idum.le.0.or.iy.eq.0) then
        idum=max(-idum,1)
        do 11 j=NTAB+8,1,-1
          k=idum/IQ
          idum=IA*(idum-k*IQ)-IR*k
          if (idum.lt.0) idum=idum+IM
          if (j.le.NTAB) iv(j)=idum
11      continue
        iy=iv(1)
      endif
      k=idum/IQ
      idum=IA*(idum-k*IQ)-IR*k
      if (idum.lt.0) idum=idum+IM
      j=1+iy/NDIV
      iy=iv(j)
      iv(j)=idum
      ran1=min(AM*iy,RNMX)
      return
      END