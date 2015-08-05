Simple commmand based encryption tool for local files.
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
