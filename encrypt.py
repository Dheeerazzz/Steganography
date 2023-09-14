import numpy as np
import PIL.Image

def encryptor(img_path='cat.png',hide_msg="Hi"):
        image=PIL.Image.open(img_path,'r')
        width,height=image.size 
        img_Arr=np.array(list(image.getdata()))
        #print(img_Arr.size)

        if image.mode=="P":
            print("Not supported")
            exit()

        channels= 4 if image.mode=="RGBA" else 3

        pixels=img_Arr.size//channels 
        stop_indicator="$NEURAL$"

        stop_indicator_length=len(stop_indicator)
        hide_msg+=stop_indicator

        byte_msg=''.join(f"{ord(c):08b}" for c in hide_msg)
        #print(byte_msg)

        bits=len(byte_msg)
        #print(bits)
        if bits>pixels:
            print("Not enogth space")
        else:
            index=0
            for i in range(pixels):
                for j in range(0,3):
                    if index<bits:
                        img_Arr[i][j]=int(bin(img_Arr[i][j])[2:-1] + byte_msg[index],2)
                        index+=1

        img_Arr=img_Arr.reshape(height,width,channels)
        results=PIL.Image.fromarray(img_Arr.astype('uint8'),image.mode)
        #results.save('encod.png')
        return results
encryptor()