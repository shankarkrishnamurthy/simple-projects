

Writer-priority readers-writers solution:
-----------------------------------------
  Hint:
    readSwitch = Lightswitch()
    writeSwitch = Lightswitch()
    noReaders = Semaphore(1)
    noWriters = Semaphore(1) 
  Reader:
    noReaders.wait()
    readSwitch.lock( noWriters )
    noReaders.signal()
        # critical section for readers
    readSwitch.unlock( noWriters )
  Writer:
    writeSwitch.lock( noReaders )
    noWriters.wait()
        # critical section for writers
    noWriters.signal()
    writeSwitch.unlock( noReaders )


