# Secure file encryption

This is a simple commmand based encryption wrapper for local files.

As it requires the Linux tools 'less' and 'nano' to work for read and write functionality,
a Linux system is required.

## Usage

It promts the user for a password (which can be empty).

The password is hashed using SHA512 and divided in 4 32-character-parts (in hex).
Each part of the password is then consecutivly used for a AES-Encryption of the given file.
Decryption is likewise.

The tool has four different modes.
Encryption / Decryption (simple as that)
Read-Mode: An encrypted file (by this tool) is temporarily decrypted (in a temp file which is erased after) and
  shown using the unix less-command. After closing less, the temp-file is erased.
Write-Mode: The encrypted file is temporarily decrypted and opened with the unix nano-command.
  After editing and closing nano (don't change the filename!) the file will be encrypted again in a new file
  with the suffix "_en".

Todo: Add some salt to Sha512 to prevent precomputed attacks on weak passwords.


Usage:
    Syntax:
        python encoder OPERATION FILE
    Valid value for OPERATION:
        -h
            prints this usage and exits
        -e | --encrypt
            encrypts the specified FILE
        -d | --decrypt
            decrypts the specified FILE
        -r | --read
            shows the content of the specified FILE after
            a decryption and encrypts the file automatically with the
            same specified password after reading.
        -w | --write
            opens the specified FILE for reading/writing after
            a decryption and encrypts the file automatically with the
            same specified password after editing.
    Valid value for FILE:
        the local path to an existing file.
