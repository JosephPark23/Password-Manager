# **Project Reflections & Updates**

### **11/3/2024**
- I'm starting this project reflections and updates file so I can better organize my ideas and tasks
  for this project. I've been working on this project for a few days already and I have a specific
  structure in mind.
#### - TODO:
    - Continue working on the hash storage and comparison functions: Need to keep updating the hash
    - Finish the rest of the architecture: the homepage interface, decision trees, and getting the passwords
    - Add exception handlers to the file opening blocks and password confirmation procedures for the vault setup file

### **11/5/2024**
- I've developed the structure more in the past few days. My plan is to create the bare, terminal-based
  manager first, then transition to a more advanced, GUI-based, feature-rich application
- I've created the authentication file but I still have work to do: I have to integrate the hash and salt
  filepath storage mechanisms into both the authentication and vault creation files, and add exception
  mechanisms to ensure smooth running
- I also have to manage the print statements and user interactions in the files themselves
##### - Some ideas I have for the future:
  - Integrate Tkinter or a GUI library to make the application more robust and accessible
  - Add a 2FA feature during authentication or such to ensure the ID of the user

### **11/12/2024**
- Today, I finished integrating the hash and salt storage files/algorithms and I now have to work on
  finishing the vault modification and view files. After I'm done with that, I should be able to move on
  to creating more advanced features, such as TKinter, 2FA, and other cool applications. I also have to add
  exception mechanisms into the code to make it more robust. 
#### - TODO:
    - Finish creating vault modification and access files
    - Add exception mechanisms to ensure robustness
    - Brainstorm more ideas for better features and security

### ***12/12/2024***
- I've finished the vault access files (I've gotten rid of the modification file for now - I don't really see a point
  in having one), and finished integrating the files and modules together, but I have so much more to do. I have to 
  replace my recursive functions with iterative loops, implement except and file handling on all functions, sanitize 
  inputs to prevent path transversal vulnerabilities, ensure cryptographic operations aren't redundant, and fix any logic/control flow issues.
#### - TODO:
    - Fix input handling: santize & secure inputs, replace recursive functions with iterative loops
    - Implement file handling try/except blocks accross files
    - Ensure logic and control are efficient and that redundancies are _nonexistent_.

### ***12/12/2024***
- Everything's finished but there are some major areas to iron out (like the access vault file which doesn't seem to be working)
  after I fix those, I'll move onto advanced features like building a CLI (and later a tkinter or directly to a tkinter), 2FA,
  input validation, and other objects. 
#### - TODO:
    - massive debugging!!!