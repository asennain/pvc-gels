def connect_keithley(ip_address: str, channels: str, data_socket): 

    from KeithleyConnect import instrument_connect, instrument_write


    """****************************INSTRUMENT SETUP****************************"""
    """***********************************************************************"""
    """*********MAKE SURE THE KEITHLEY IS SET TO SCPI TO COMMUNITCATE*********"""
    """***********************************************************************"""
    """****************************INSTRUMENT CONNECTION****************************"""
    #! Go into Windows and set the Ethernet connection to manual 
    # define the instrament's IP address. the port is always 5025 for LAN connection.
    # establish connection to the LAN socket. initialize and connect to the Keithley
          # Close the connection if one already exists 
      # Establish a TCP/IP socket object
    instrument_connect(data_socket, ip_address, 5025, 10000, 0, 1) 

    """***************INSTRUMENT SET UP***************"""
    # reset the device
    instrument_write(data_socket, "*RST")

    # define the measurement channels
  
    channel_count = len(channels.split(','))

    # define the scan list, set scan count to infinite, and channel delay of 75 um
    instrument_write(data_socket, ":ROUTe:SCAN:CRE (@{0})".format(channels)) # Create channels
    instrument_write(data_socket, ":ROUTe:SCAN:COUN:SCAN 0") # Infinite scan count
    instrument_write(data_socket, ":ROUTe:DEL 0.0002, (@{0})".format(channels)) # Channel delay
    instrument_write(data_socket, ":ROUTe:SCAN:INT .05") # Scan to scan interval 

    # choose the buffer and assign all data to the buffer after clearing it
    instrument_write(data_socket, "TRACe:CLEar") 
    instrument_write(data_socket, ":TRAC:FILL:MODE CONT, \"defbuffer1\"")
    instrument_write(data_socket, ":ROUT:SCAN:BUFF \"defbuffer1\"")

    # # define the channel functions
    instrument_write(data_socket, "FUNC 'VOLT:DC', (@{0})".format(channels)) 

    # # define channel parameters such as range to 1 volt, autozero off, and line sync on
    instrument_write(data_socket, "VOLT:DC:RANG 1, (@{0})".format(channels)) # Range
    instrument_write(data_socket, "VOLT:DC:AZER OFF, (@{0})".format(channels)) # Auto-zero off
    instrument_write(data_socket, "VOLT:DC:LINE:SYNC ON, (@{0})".format(channels)) # Line sync on 
    instrument_write(data_socket, "VOLT:DC:DEL:AUTO ON, (@{0})".format(channels)) # Auto-delay off
    instrument_write(data_socket, ":SENS:VOLT:DC:NPLC 1, (@{0})".format(channels)) # NPLC
    instrument_write(data_socket, "VOLT:DC:INP MOHM10, (@{0})".format(channels)) # Input impedance

    # enable the graph to plot the data
    instrument_write(data_socket, ":DISP:SCR HOME")
    instrument_write(data_socket, "DISP:WATC:CHAN (@108)")  #!! Hard-coded watch channel 108
    instrument_write(data_socket, ":DISP:SCR GRAP")












def stop_trail_export_csv(file_name, directory_name, data_socket, channels):
    from KeithleyConnect import instrument_query,instrument_write
    import csv
        
    channel_count = len(channels.split(','))

    while 1 == 1:
        if int(instrument_query(data_socket, "TRACe:ACTual:END? \"defbuffer1\"", 16).rstrip()) % channel_count == 0:       
            instrument_write(data_socket,"ABORT")
            break
        
    # identify how many readings there are
    readings_count = int(instrument_query(data_socket, "TRACe:ACTual?", 16).rstrip())

    # preallocate counters and a Data list 
    start_index = 1
    end_index = channel_count
    accumulated_readings = 0
    Data = []

    # read the buffer and place measurements into the 
    while accumulated_readings < readings_count:
        Data.append(instrument_query(data_socket, "TRACe:DATA? {0}, {1}, \"defbuffer1\", REL, READ".format(start_index, end_index), 128).split(','))
        start_index += channel_count
        end_index += channel_count
        accumulated_readings += channel_count
        
    newFile = open('{0} {1}.csv'.format(directory_name, file_name),'w',newline='')
    newWriter = csv.writer(newFile, dialect='excel')
    for i in range(len(Data)):
        if i > 1:
            newWriter.writerow(Data[i])
    newFile.close()



