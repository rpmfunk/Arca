from cryptography.fernet import Fernet
import os
from os.path import exists


def getRawKey(key_file):
    return readFromFile(key_file)


def getKey(key_file):
    """
    WARNING: New key will be made (and potentially overwrite old file) if key cannot be loaded
    """
    try:
        key = readFromFile(key_file)
        return Fernet(key)
    except Exception as e:
        print("Could not locate encryption key. Creating a new one...")
        key = makeKey()
        saveKey(key, key_file)
        return Fernet(key)


def splitPath(file_path):
    return '/'.join(file_path.split('/')[:-1])


def makePath(file_path):
    working_path = splitPath(file_path)
    if not os.path.exists(working_path):
        os.makedirs(working_path)


def makeKey():
    return Fernet.generate_key()


def saveKey(key, filename):
    writeToFile(text=key.decode('utf-8'), filename=filename)


def writeToFile(text, filename):
    makePath(filename)
    f = open(filename, 'w+')
    f.write(text)
    f.close()


def readFromFile(filename):
    with open(filename, 'r') as f:
        text = f.read()
    return text


def backupFile(filename):
    copyFile(filename, '{}.bk'.format(filename))


def copyFile(filename, new_filename):
    text = readFromFile(filename)
    writeToFile(text=text, filename=new_filename)


class Encryption:
    def __init__(self, key=None, key_file=None):
        if key:
            self.key = Fernet(key)
        self.key_file = key_file
        if self.key_file:
            self.key = getKey(self.key_file)  # Fernet object

    def encryptText(self, text):
        token = self.key.encrypt(bytes(text, encoding='utf8'))
        # return token.encode('unicode_escape')
        return token.decode('utf-8')

    def decryptText(self, text):
        text = self.key.decrypt(bytes(text, encoding='utf8'))
        # return text.encode('unicode_escape')
        return text.decode('utf-8')

    def encryptFile(self, text, filename):
        text = self.encryptText(text)
        writeToFile(text=text, filename=filename)

    def encryptFileInPlace(self, filename):
        text = readFromFile(filename)
        os.remove(filename)
        self.encryptFile(text=text, filename=filename)

    def decryptFileInPlace(self, filename):
        text = self.decryptFile(filename=filename)
        os.remove(filename)
        writeToFile(text=text, filename=filename)

    def decryptFile(self, filename):
        text = readFromFile(filename=filename)
        return self.decryptText(text)

    def makeTemporaryFile(self, permFileName, tempFileName):
        text = readFromFile(permFileName)
        text = self.decryptText(text)
        writeToFile(text=text, filename=tempFileName)

    def backToPermFile(self, permFileName, tempFileName, deleteTempFile=False):
        text = readFromFile(tempFileName)
        text = self.encryptText(text)
        writeToFile(text=text, filename=permFileName)
        if deleteTempFile:
            os.remove(tempFileName)
