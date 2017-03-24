@echo off
setlocal enableextensions enabledelayedexpansion
call:main %* & goto:EOF
::-----------------------------------------------------------------------

:main
	::var
	set input=%*

	if not "%input%"=="" (
		set arg=;%input%
	) else (
		call:burn
	)

	::workflow
		REM call:burn
		call:format
		call:2json %arg%
	goto:EOF

	:burn
		::list wmic commands [;rol_accion_atributo,atributo,atributo,...;rol_accion_atributo,atributo,atributo,...]

		REM set arg=%arg%;COMPUTERSYSTEM Name,Domain,Manufacturer,Model,TotalPhysicalMemory
		REM set arg=%arg%;OS BuildNumber,Caption,Description,InstallDate,OSArchitecture,RegisteredUser,SerialNumber
		REM set arg=%arg%;BASEBOARD Manufacturer,Product,SerialNumber
		REM set arg=%arg%;CPU Name,L2CacheSize,L3CacheSize,Manufacturer,MaxClockSpeed,NumberOfLogicalProcessors,NumberOfCores,ProcessorId,SocketDesignation
		REM set arg=%arg%;MEMORYCHIP BankLabel,Capacity,DeviceLocator,FormFactor,Manufacturer,Model,SerialNumber,Speed
		set arg=%arg%;DISKDRIVE Description,Index,InterfaceType,Model,Size,SerialNumber
		set arg=%arg%;NICCONFIG Description,DefaultIPGateway,DNSServerSearchOrder,Index,IPAddress,IPSubnet,MACAddress
		REM set arg=%arg%;PARTITION BlockSize,Bootable,BootPartition,DeviceID,NumberOfBlocks,PrimaryPartition,Size,StartingOffset,Type
		REM set arg=%arg%;VOLUME Automount,BootVolume,Capacity,Compressed,FileSystem,FreeSpace,Label,SerialNumber,SystemVolume

	 	set arg=%arg%;PRODUCT InstallSource,InstallDate,LocalPackage,Name,Vendor,Version

		REM set arg=%arg%;CDROM Name,MediaType,VolumeName,Size
		REM set arg=%arg%;DESKTOPMONITOR MonitorManufacturer,Name,ScreenHeight,ScreenWidth
		REM set arg=%arg%;SOUNDDEV Name,Manufacturer,DeviceID

		REM set arg=%arg%;PORTCONNs22ECTOR InternalReferenceDesignator

		REM set arg=%arg%;PRINTER CapabilityDescriptions,DeviceID,PrintProcessor

		REM set arg=%arg%;SHARE Caption,Name,Path
		REM set arg=%arg%;USERACCOUNT Description,Disabled,Domain,FullName,LocalAccount,Name,PasswordChangeable,PasswordExpires,PasswordRequired,SID,Status

		goto:EOF

	:format
		set arg=%arg:wmic=%
		set arg=%arg:get=%
		set arg=%arg: =_%
		::lock list
		set arg=%arg:,=-%
		goto:EOF

	:2json
		::IN: list wmic commands [;rol_accion_atributo,atributo,atributo,...;rol_accion_atributo,atributo,atributo,...]
		::args
		set in=%*
		REM set out=%2

		::lock list
		set in=%in:,=-%

		::rol length
		set /a count=0
		for %%a in (%in%) do (set /a count=count+1)

		::split list
		set onetime=0
		for %%a in (%in%) do (
			::unlock lists
			set commd=%%a& set commd=!commd:-=,!

			::read wmic command of list
			for /f "tokens=1-2 delims=_" %%a in ("!commd!") do (
				set rol=%%a
				set action=get
					if [!rol!]==[NICCONFIG] (
						set action=where "MACAddress is not null and IPEnabled=TRUE" get
					)
				set property=%%b

				::opening json
				if [!onetime!]==[0] (
					echo {
					set onetime= 1
				)

				::print rol
				echo "!rol!": [

				::property length
				set /a count2=0
				for %%o in (!property!) do (set /a count2=!count2!+1)
				set /a rstcount2=!count2!

				::instace property length
				set /a count3=0
				for /f "usebackq" %%x in (`wmic !rol! !action! !property! /format:list^|find "="`) do (set /a count3=count3+1)

				::execute wmic command
				for /f "usebackq tokens=1-2 delims==" %%x in (`wmic !rol! !action! !property! /format:list^|find "="`) do (

					::delete carrier return for value
					set y=%%y& set y=!y:~0,-1!
					::protected null value
					set y="!y!"

					::rules format
					set y=!y:\=\\!
					set y=!y:"{=[!
					set y=!y:}"=]!

					::delete large blank spaces
					set v=!y!
						set y=!y:   =!
						if not [!y!]==[!v!] (
							set y=!y: =!
						)

					::format property & value
					set property=		"%%x": !y!

					::print property
					if !count2!==!rstcount2! (echo 	{)
					::property separator
					if !count2! equ 1 (
						echo !property!
						::print close group property
						if !count3! equ 1 (echo 	}) else (echo 	},)
						::reset list concatenate property
						set /a count2=!rstcount2!
					) else (
						echo !property!,
						::count separator property
						set /a count2=!count2!-1
					)

					::count separator group property
					set /a count3=!count3!-1
				)
				::print rol's end
				if !count! equ 1 (
					echo 	]
				) else (
					echo 	],
					::count separator property
					set /a count=count-1
				)
			)
		)
		echo }
goto:EOF
