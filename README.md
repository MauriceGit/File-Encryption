# Secure File Encryption

This is a simple commmand based encryption wrapper for local files.

As it requires the Linux tools 'less' and 'nano' to work for read and write functionality,
a Linux system is required.

## General information

It promts the user for a password (which can be empty).

The password is hashed using SHA512 hashing algorithm and divided in four 32-character-parts (in hex).

Each part of the password is then consecutively used for a AES-256 encryption of the given file.
Decryption works likewise.

## Usage

The tool has four different modes.

- Encryption / Decryption: Encrypts or decrypts a given file with a given password.

- Read-Mode: An encrypted file (by this tool) is temporarily decrypted (in a temp file which is erased after) and
  shown using the Linux 'less' command. After closing less, the temp file is erased.
  No changes are done to the original encrypted file.

- Write-Mode: The encrypted file is temporarily decrypted and opened with the Linux 'nano' command.
  After editing and closing nano (don't change the filename!) the file will be encrypted again in a new file
  with the added suffix "_en".

Type an invalid command or "-h" to get the exact usage and syntax.

## Further Improvements

Add some salt to Sha512 to prevent precomputed attacks on weak passwords.

