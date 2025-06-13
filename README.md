# VM installation (Αν έχετε ήδη εγκατεστημένα Linux, πηγαίνετε κατευθείαν στο Εγκατάσταση του Contiki-NG σε Linux)

 Σε περίπτωση που δεν έχετε εγκατεστημένα Linux (και δεν επιθυμείτε να εγκαταστήσετε) ή MacOS, προτείνουμε να χρησιμοποιήσετε ένα από τα δύο VM για Windows και να εγκαταστήσετε ένα Linux image σε αυτά (προτείνουμε Ubuntu 22.04 LTS ή Ubuntu 20.04 LTS):
 1.   VMWare (recommended, αν είναι εφικτό)
 2.   VirtualBox

## Προβλήματα εγκατάστασης Ubuntu σε VirtualBox VM

Αν εγκαταστήσετε Ubuntu σε VirtualBox, πιθανό να αντιμετωπίσετε μία σειρά από προβλήματα:

### *Δεν ανοίγει το Terminal*

Σε αυτή τη περίπτωση, πρέπει να ακολουθήσετε τα παρακάτω βήματα:
	1.1    Στο login screen των Ubuntu πατίστε τα κουμπιά Ctrl+Alt+F5, για να σας βγάλει στο Terminal. Εκεί, θα χρειαστεί να συνδεθείτε με το username και password των Ubuntu που έχετε θέσει κατά την εγκατάσταση
	2.1    Εκτελέστε τα παρακάτω **(Αν δεν δουλεύει το sudo, πηγαίνετε στο πρόβλημα 2, λύστε το και επανέλεθετε σε αυτό το βήμα)**:
```bash
    sudo nano /etc/default/locale
    # Στην πρώτη γραμμή, αλλάξτε το en_US σε en_US.UTF-8
    # Ctrl+X για να βγείτε από το nano editor και save
    sudo locale-gen --purge
	reboot
```

### *Δε λειτουγεί το sudo*. 

Σε αυτή τη περίπτωση, ακολουθείστε τα βήματα του [guide](https://www.tecmint.com/fix-user-is-not-in-the-sudoers-file-the-incident-will-be-reported-ubuntu/)


# Εγκατάσταση του Contiki-NG σε Linux

Πρωτού κάνετε οτιδήποτε, καλό είναι να δημιουργήσετε ένα φάκελο στον οποίο θα αποθηκεύσετε τα απαραίτητα αρχεία που πρέπει να κατεβάσετε, καθώς και το Contiki-NG. Για παράδειγμα, δημιουργήστε ένα νέο φάκελο στο φάκελο Downloads και εισέλθετε σε αυτόν. Στο terminal, εκτελέστε τα παρακάτω:

```bash
    mkdir ~/Downloads/<το_όνομα_του_φακέλου>
    cd ~/Downloads/<το_όνομα_του_φακέλου>
```

## Install development tools for Contiki-NG

Στο terminal, εκτελέστε τις παρακάτω εντολες:

```bash
    sudo apt update
    sudo apt install build-essential doxygen git git-lfs curl wireshark python3-serial srecord rlwrap
    sudo usermod -a -G wireshark <your_user_name>  # an error might occur, don't bother
```

## Install ARM compiler
Στο terminal, βεβαιωθείτε ότι είστε στον φάκελο στον οποίο κατεβάζετε τα διάφορα αρχεία και εκτελέστε τα παρακάτω:
```bash
    cd ~/Downloads/<το_όνομα_του_φακέλου>
    wget https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu-rm/9-2020q2/gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2
    tar -xjf gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2
```

Στη συνέχεια, πρέπει να γίνει export του path του φακέλου με τα εκτελέσιμα αρχεία στο PATH. Αρχικά, πρέπει να βρείτε το path του αρχείου με τα εκτελέσιμα:

```bash
    cd ~/Downloads/<το_όνομα_του_φακέλου>/gcc-arm-none-eabi-9-2020-q2-update/bin
    pwd     # Αυτή η εντολή θα εκτυπώσει το path του φακέλου με τα εκτελέσιμα
```

Στη συνέχεια, υπάρχουν δύο τρόποι για να γίνει το export:

### Τρόπος 1: Export "in-place"
Εκτελέστε το παρακάτω βήμα:
```bash
    export PATH=$PATH:<το_path_που_βρήκατε_από τη_pwd>
```

Το πρόβλημα με αυτή τη μέθοδο είναι ότι θα πρέπει να εκτελείτε τα παραπάνω βήματα κάθε φορά που ανοίγετε το VM.

### Τρόπος 2: Αλλαγή του .bashrc (recommended)

Εκτελέστε τα παρακάτω βήματα:

```bash
    sudo nano ~/.bashrc
    # Στο τέλος του αρχείου, προσθέστε τη παρακάτω εντολή:
    export PATH=$PATH:<το_path_που_βρήκατε_από τη_pwd>
    # Save and exit
```

Με αυτή τη μέθοδο κάθε φορά που ανοίγετε το VM θα είναι ο φάκελος κατευθέιαν φορτωμένος στο PATH

## Install MSP430 compiler
Ανοίξτε το terminal, πλοηγηθείτε στον φάκελο που κατεβάζετε τα αρχεία και εκτελέστε την παρακάτω εντολή:

```bash
    sudo wget -nv http://simonduq.github.io/resources/mspgcc-4.7.2-compiled.tar.bz2 && \
        sudo tar xjf mspgcc*.tar.bz2 -C /tmp/ && \
        sudo cp -f -r /tmp/msp430/* /usr/local/ && \
        sudo rm -rf /tmp/msp430 mspgcc*.tar.bz2
```

## User access to USB
Εκτελέστε τις παρακάτω εντολές
```bash
    sudo usermod -a -G plugdev <το_όνομα_user>
    sudo usermod -a -G dialout <το_όνομα_user>
```

## Reboot τα Linux
Πρέπει να κάνετε reboot για να γίνουν όλες οι αλλαγές

## Clone Contiki-NG
Αφού ξανανοίξουν τα Linux, ανοίξτε το terminal, οδηγηθείτε στο φάκελο που κατεβάζετε τα διάφορα αρχεία και κατεβάστε το Contiki-NG
```bash
    cd ~/Downloads/<το_όνομα_του_φακέλου>/
    git clone https://github.com/contiki-ng/contiki-ng.git
    cd contiki-ng
    git submodule update --init --recursive     # Αυτό το βήμα θα πάρει ώρα
```

## Install απαραίτητες βιβλιοθήκες (για Linux x64-bit, αν είναι απαραίτητο)

Αν το compile και upload αποτύχουν λόγω dependencies για το sky architecture το Contiki-NG, τότε είναι απαραίτητο να εγκατασταθούν κάποιες βιβλιοθήκες για αρχιτεκτονικές x32-bit, έτσι ώστε να μπορεί να γίνει το compilation για sky architercture, σε περίπτωση που έχετε εγκατεστημένα Linux χ64-bit (το ποιο πιθανό).

Σε αυτή τη περίπτωση, εκτελέστε τα παρακάτω:
```bash
    sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1:i386
```
Μπορεί κάποιες από αυτές τις βιβλιοθήκες να μην κατέβουν, οπότε ενδεχομένως να μην έχετε περαιτέρω προβλήματα. Εξαρτάται από την έκδοση των Linux χρησιμοποιείται

## python.Serial

Αν το compile αποτύχει λόγω τις βιβλιοθήκης Serial της Python, τότε πρέπει να εκτελέσετε τα παρακάτω:

```bash
	pip uninstall pyserial
	pip install pyserial
```
ή

```bash
	pip uninstall pyserial3
	pip install pyserial3
```

# Σχόλια φοιτητή για τα βήματα που ακολουθήθηκαν

## Η εργασία υλοποιείται σε περιβάλλον Ubuntu 22.04 LTS το οποίο τρέχει μέσα σε VMWare εικονική μηχανή.

Δημιουργήσαμε έναν φάκελο "sensors" στο Downloads directory και εγκαταστήσαμε τα απαραίτητα εργαλεία εντός αυτού.

### Ερώτημα 1 (Προγραμματισμός και εγκατάσταση των motes).

1. Tρέξιμο του παραδείγματος hello-world και επιβεβαίωση της ορθής λειτουργίας των εργαλείων.

2. a.
- Σύνδεση του TelosB με το σύστημα μας στο port /dev/ttyUSB0.
- Εγκαταστάθηκε και χρησιμοποιήθηκε το εργαλείο screen για την προβολή των μηνυμάτων.
- Προστέθηκε `LOG_INFO_LLADDR(&linkaddr_node_addr);` μέσα στην `while` του αρχείου `nullnet-unicast.c` για να εμφανιστεί η διεύθυνση MAC.
- Ο κόμβος που λειτούργησε ως κεντρικός είχε MAC: `a9b0.6013.0074.1200`
