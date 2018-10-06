import numpy as np
import matplotlib.pyplot as plt

def main():
    fs = 40 #MHz - sampling frequency
    fo = 13 #Mhz - signal frequency
    N = (fs/fo)*10 #choose N so that we can select number of periods
    L = 10 #interpolation factor
    n = np.arange(N) # N number of bins, [0,1,..., N-1]
    t = n/fs #multiple times sampling frequency to get time
    x = np.cos(2*np.pi*fo/fs*n) #sample  
    k = np.copy(n) # frequency bins [0,1,..., N-1]
    frq = k*fs/(N-1) 

    Fx = np.fft.fft(x) #FFT 
    Fxp = np.copy(Fx) #create copy, not 
    
    #apply zero pad - (L-1)*N times 
    for i in range(int((L-1)*N)):
        mid_bin = int(np.size(Fxp)/2)
        Fxp = np.insert(Fxp,mid_bin,np.complex(0,0))

    xp = L*np.real(np.fft.ifft(Fxp))
    Np = np.size(xp)
    tp = np.arange(Np)/fs/L
    kp = np.arange(Np)
    frqp = kp*fs*L/(Np - 1)

    #find zero crossings of with positive slope
    z0 = None 
    z1 = None
    for i in range(1,Np):
        if(z0 == None):
            if((xp[i] > 0.0) and (xp[i-1] <= 0.0)):
                z0 = i
        else:
            if(z1 == None):
                if((xp[i] > 0.0) and (xp[i-1] <= 0.0)):
                    z1 = i

    #Zero Crossing Period Approximation 
    T = tp[z1] - tp[z0]
    print("[DBG] Using zero crossings to estimate frequency")
    print("Period=%f"%(T))
    print("Frequency=%f"%(1/T))

    #look at first half < Fs/2
    frq = frq[range(int(N/2))]
    Fx = Fx[range(int(N/2))]
    
    #zero pad, look at first half 
    frqp = frqp[range(int(Np/2))]
    Fxp = Fxp[range(int(Np/2))]

    #create plots of signal before and after interpolation 
    plt.figure(1)

    #original time domain
    plt.subplot(221)
    plt.plot(t,x)

    #original fft
    plt.subplot(222)
    plt.plot(frq,abs(Fx))

    #interpolated signal
    plt.subplot(223)
    plt.plot(tp,xp)

    #zero pad fft
    plt.subplot(224)
    plt.plot(frqp,abs(Fxp))
    plt.show()

if __name__ == "__main__":
    main()