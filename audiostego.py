from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
from pydub import AudioSegment
import numpy as np
import os

class AudioStegano:
    output_audio_size = 0

    # Main frame or start page
    def main(self, root):
        root.title('Audio Steganography')
        root.geometry('500x600')
        root.resizable(width=True, height=True)
        root.config(bg='#e3f4f1')
        frame = Frame(root)
        frame.grid()

        title = Label(frame, text='Audio Steganography')
        title.config(font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        title.grid(pady=10)
        title.grid(row=1)

        encode = Button(frame, text="Encode", command=lambda: self.encode_frame1(frame), padx=14, bg='#e3f4f1')
        encode.config(font=('Helvetica', 14), bg='#e8c1c7')
        encode.grid(row=2)
        decode = Button(frame, text="Decode", command=lambda: self.decode_frame1(frame), padx=14, bg='#e3f4f1')
        decode.config(font=('Helvetica', 14), bg='#e8c1c7')
        decode.grid(pady=12)
        decode.grid(row=3)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    # Back function to loop back to main screen
    def back(self, frame):
        frame.destroy()
        self.main(root)

    # Frame for encode page
    def encode_frame1(self, F):
        F.destroy()
        F2 = Frame(root)
        label1 = Label(F2, text='Select the Audio file in which \nyou want to hide text:')
        label1.config(font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()

        button_bws = Button(F2, text='Select', command=lambda: self.encode_frame2(F2))
        button_bws.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_bws.grid()
        button_back = Button(F2, text='Cancel', command=lambda: AudioStegano.back(self, F2))
        button_back.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(pady=15)
        button_back.grid()
        F2.grid()

    # Frame for decode page
    def decode_frame1(self, F):
        F.destroy()
        d_f2 = Frame(root)
        label1 = Label(d_f2, text='Select Audio file with Hidden text:')
        label1.config(font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()
        label1.config(bg='#e3f4f1')
        button_bws = Button(d_f2, text='Select', command=lambda: self.decode_frame2(d_f2))
        button_bws.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_bws.grid()
        button_back = Button(d_f2, text='Cancel', command=lambda: AudioStegano.back(self, d_f2))
        button_back.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(pady=15)
        button_back.grid()
        d_f2.grid()

    # Function to encode audio
    def encode_frame2(self, e_F2):
        e_pg = Frame(root)
        myfile = tkinter.filedialog.askopenfilename(filetypes=[('wav', '*.wav'), ('mp3', '*.mp3'), ('All Files', '*.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            self.audio_path = myfile
            label3 = Label(e_pg, text='Selected Audio')
            label3.config(font=('Helvetica', 14, 'bold'))
            label3.grid()
            label2 = Label(e_pg, text='Enter the message')
            label2.config(font=('Helvetica', 14, 'bold'))
            label2.grid(pady=15)
            text_a = Text(e_pg, width=50, height=10)
            text_a.grid()
            encode_button = Button(e_pg, text='Cancel', command=lambda: AudioStegano.back(self, e_pg))
            encode_button.config(font=('Helvetica', 14), bg='#e8c1c7')
            encode_button.grid()
            button_back = Button(e_pg, text='Encode', command=lambda: [self.enc_fun(text_a), AudioStegano.back(self, e_pg)])
            button_back.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back.grid(pady=15)
            e_pg.grid(row=1)
            e_F2.destroy()

    # Function to decode audio
    def decode_frame2(self, d_F2):
        d_F3 = Frame(root)
        myfiles = tkinter.filedialog.askopenfilename(filetypes=[('wav', '*.wav'), ('mp3', '*.mp3'), ('All Files', '*.*')])
        if not myfiles:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            hidden_data = self.decode(myfiles)
            label2 = Label(d_F3, text='Hidden data is:')
            label2.config(font=('Helvetica', 14, 'bold'))
            label2.grid(pady=10)
            text_a = Text(d_F3, width=50, height=10)
            text_a.insert(INSERT, hidden_data)
            text_a.configure(state='disabled')
            text_a.grid()
            button_back = Button(d_F3, text='Cancel', command=lambda: self.frame_3(d_F3))
            button_back.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back.grid(pady=15)
            d_F3.grid(row=1)
            d_F2.destroy()

    # Function to encode data into audio
    def enc_fun(self, text_a):
        data = text_a.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            audio = AudioSegment.from_file(self.audio_path)
            sample_rate = audio.frame_rate
            samples = np.array(audio.get_array_of_samples())

            # Encode data
            data_bin = ''.join(format(ord(i), '08b') for i in data)
            data_bin += '1111111111111110'  # End of data marker

            # Make sure we have enough samples to encode data
            if len(data_bin) > len(samples):
                messagebox.showerror("Error", "Text is too long to encode in this audio file")
                return

            encoded_samples = np.copy(samples)
            for i in range(len(data_bin)):
                encoded_samples[i] = (encoded_samples[i] & ~1) | int(data_bin[i])

            encoded_audio = audio._spawn(encoded_samples.tobytes())
            temp = os.path.splitext(os.path.basename(self.audio_path))[0]
            save_path = tkinter.filedialog.asksaveasfilename(
                initialfile=temp,
                filetypes=[('wav', '*.wav')],
                defaultextension=".wav"
            )
            if save_path:
                encoded_audio.export(save_path, format="wav")
                self.d_audio_size = os.path.getsize(save_path)
                self.d_audio_duration = len(encoded_audio) / 1000
                messagebox.showinfo("Success", "Encoding Successful\nFile is saved successfully.")

    # Function to decode data from audio
    def decode(self, audio_path):
        audio = AudioSegment.from_file(audio_path)
        samples = np.array(audio.get_array_of_samples())
        data_bin = ''

        for sample in samples:
            data_bin += str(sample & 1)

        data_chars = [chr(int(data_bin[i:i+8], 2)) for i in range(0, len(data_bin), 8)]
        data = ''.join(data_chars)

        end_marker = data.find(chr(0xFF))  # Look for the end marker
        if end_marker != -1:
            data = data[:end_marker]

        return data

    def frame_3(self, frame):
        frame.destroy()
        self.main(root)


# GUI loop
root = Tk()
o = AudioStegano()
o.main(root)
root.mainloop()


