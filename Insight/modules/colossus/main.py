import getopt, sys
import os
import boto3
import encrypt, decrypt, upload, mail


def main():
    type = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "t:h:")

    except:
        print ("usage: python3 main.py -t upload")
        print ("usage: python3 main.py -t download")
        print("usage: python3 main.py -t decrypt")
        sys.exit(2)

    else:
        for opt, arg in opts:
            if opt in ['-h']:
                print ("usage: python3 main.py -t upload")
                print ("usage: python3 main.py -t download")
                print ("usage: python3 main.py -t decrypt")
                os._exit(0)

            elif opt in ['-t']:
                type = arg

        if (type == "upload"):
            bucket = input("Enter bucket name: ")
            src = input("Enter input file name: ")
            object = input("Enter output file name: ")
            encrypt.mainMenu(src, object)
            upload.upload_file(src, bucket, object)
            mail.mail()
            print("Uploaded Successfully!!!")

        elif (type == "download"):
            bucket = input("Enter bucket name: ")
            src = input("Enter save path: ")
            object = input("Enter object name: ")
            s3 = boto3.client('s3')
            s3.download_file(bucket, object, src)
            print("File Downloaded!!!")

        elif (type == "decrypt"):
            input_filename = input("Enter input file name: ")
            output_filename = input("Enter output file name: ")
            decrypt.decrypt(input_filename, output_filename)

if __name__ == '__main__':
    main()