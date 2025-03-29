from numpy import convolve
from matplotlib import pyplot as plt
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv  

# @brief This function calculates the convolution of two vectors
# @param x,y input vectors
# @return convolution of x and y
def myConv(x, y,x_len,y_len):
    x_len = len(x)
    y_len = len(y)

    # create a list to store the convolution results
    result = [0] * (x_len + y_len - 1)

    # iterate over the y vector with the x vector
    for i in range(x_len):
        for j in range(y_len):
            result[i + j] += x[i] * y[j]
    return result

# @brief This function plots X and Y Vectors + the results of the convolutions of x and y vectors
# @param x,x_0 : X vector and the element's index which located at (x-axis 0)
#        y,y_0 : Y vector and the element's index which located at (x-axis 0)
#        my_conv_result : result of convolution of x and y vectors with my function
#        numpy_conv_res : result of convolution of x and y vectors with numpy library
#        shift : on the stem graph shift the x-axis to the given value (* -1 for the correct direction)
#
def plot_results(x,x_0,y,y_0,my_conv_result,numpy_conv_res,shift):

    shift = int(shift) * -1
    x_0 = int(x_0) * -1
    y_0 = int(y_0) * -1


    print("Shift: ",shift)

    plt.subplot(2,2,1)
    plt.stem(range(x_0,x_0+len(x)), x)
    plt.xlim(-5,5)
    plt.xlabel('x')
    plt.ylabel('Amplitude')
    plt.title('X Vector')
    plt.xticks(range(x_0,x_0+len(x)))
    plt.yticks(x)
    plt.grid()

    plt.subplot(2,2,2)
    plt.stem(range(y_0,y_0+len(y)), y)
    plt.xlim(-5,5)
    plt.xlabel('x')
    plt.ylabel('Amplitude')
    plt.title('Y Vector')
    plt.xticks(range(y_0,y_0+len(y)))
    plt.yticks(y)
    plt.grid()

    plt.subplot(2,2,3)
    plt.stem(range(shift,len(my_conv_result)+shift), my_conv_result)
    plt.xlim(-10,10)
    plt.title('Convolution of x and y (My Function)')
    plt.xlabel('x')
    plt.ylabel('Amplitude')
    plt.xticks(range(shift,len(my_conv_result)+shift))
    plt.yticks(my_conv_result)
    plt.grid()

    plt.subplot(2,2,4)
    plt.stem(range(shift,len(numpy_conv_res)+shift), numpy_conv_res)
    plt.xlim(-10,10)
    plt.title('Convolution of x and y (Numpy Library)')
    plt.xlabel('x')
    plt.ylabel('Amplitude')
    plt.xticks(range(shift,len(numpy_conv_res)+shift))
    plt.yticks(numpy_conv_res)
    plt.grid()

    plt.subplots_adjust(hspace=.325, wspace=.425, top=.95, bottom=0.07, left=0.125, right=0.9)
    plt.show()

    return

# @brief This function records the voice for the given seconds
# @param seconds : the duration of the recording
# @return the recording as a numpy array (1D)
def record_voice(seconds = 5):
    
    fs = 8100  # Sample rate

    my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write('my_recording.wav', fs, my_recording)  # Save recording as a WAV file

    return my_recording.flatten()

# @brief This function plays the given recording
# @param recording : the recording to be played
#        fs : sample rate of the recording
def play_record(recording,fs=8100):
    sd.play(recording, fs)
    sd.wait()

# @brief  This function calculates the h vector using the given function on the paper
# @param  x : input vector
#         M : the number of inner iterations
# @return h vector which is calculated using the given function on the paper
def calculate_h(x,M=3):
    h = x
    for index in range(len(x)):
        for k in range(1,M+1):
            h[index] = (2**(-k)) * k * h[index-3000*k] 
    return h   

def main():
    
    # input of x and y vectors which will be used in the calculations
    x = input("Enter the X vector (separate with space): ")
    x = x.split(" ")
    x = [float(i) for i in x]

    x_0 = input("Enter the element's index which located at (x-axis 0): ")

    y = input("Enter the Y vector (separate with space): ")
    y = y.split(" ")
    y = [float(i) for i in y]

    y_0 = input("Enter the element's index which located at (x-axis 0): ")

    x_len = len(x)
    y_len = len(y)

    # if x is longer than y, we'll take the x_0 as the zero axis
    # so that we'll be able to plot the results correctly (on the graph)
    if x_len < y_len:
        conv_result_zero_axis = y_0
    else:
        conv_result_zero_axis = x_0

    my_result_conv = myConv(x, y,x_len,y_len)
    print("For my function result of convolution of x and y vectors is: ", my_result_conv)

    numpy_result_conv = convolve(x, y, mode='full')
    print("Numpy Library result of convolution of x and y vectors is: ", numpy_result_conv)

    plot_results(x,x_0,y,y_0,my_result_conv,numpy_result_conv,conv_result_zero_axis)

    sec = int(input("Enter how many seconds you want to record your voice (default is 5): "))

    input(f"Press anything to record your voice for {sec} seconds")
    recording_1 = record_voice(sec)
    input("Recording is done. Press anything to listen the recording")
    play_record(recording_1,8100)

    input("Press anything to see the plot of the recording")

    plt.plot(recording_1)
    plt.title(f"{sec} seconds recording")
    plt.show()

    M = int(input("Please enter the value of M for the h vector calculation (default is 3):"))

    print(f"Calculating h vector for {sec} seconds recording")
    h = calculate_h(recording_1,M)
    print("h vector is calculated.")
    ch = input("Do you want to use my function or numpy library for convolution? (Press anything for my function, press 'n' for numpy library)")
    print("Calculating the convolution of the recording and h vector. Please wait...")
    if ch != 'n':
        convResult = myConv(recording_1,h,len(recording_1),len(h))
    else :
        convResult = convolve(recording_1,h,mode='full')
    print("Convolution is done.")
    input("Press anything to listen recording BEFORE Convolution.")
    play_record(recording_1,8100)
    input("Press anything to listen recording AFTER Convolution.")
    play_record(convResult,8100)
    
    plt.plot(convResult)
    plt.title("Convolution Result of the Recording")
    plt.show()

main()