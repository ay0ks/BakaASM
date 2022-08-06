	_using $:enumerate
	_using $:lua
	_using $:sol
.data
		L#None := sol::state
		test_var#None := 10
.text
		L:open_lib(sol::lib::base, sol::lib::package)
		i := 0
		jmp _EKl465Y1Hqk#u#GRTRAY
:_EKl465Y1Hqk#u#GRTRAY
		jmp:neq!(i, math:fac(999)) _NF2DwrRPOzKVSCIUhW$g
		jmp _iz6PVOZs$iznQ3$I1YXd
:_NF2DwrRPOzKVSCIUhW$g
		_printf <u8>'%d left':fmt!(test_var)
		add! i, 1
		jmp _EKl465Y1Hqk#u#GRTRAY
:_iz6PVOZs$iznQ3$I1YXd
		del i
		cx := 0
		jmp _Myx@@R9#3iL1ji#uQTT@
:_Myx@@R9#3iL1ji#uQTT@
		jmp:neq!(cx, math:fac(999)) _63WMRLe$$H@twAENyCIv
		jmp _AX4ia$@$VAr2rc402hML
:_63WMRLe$$H@twAENyCIv
		_printf <u16>'%d манул':fmt!(test_var, (test_var:size(), leq! 4) ? 'а' : 'ов')
		add! cx, 1
		jmp _Myx@@R9#3iL1ji#uQTT@
:_AX4ia$@$VAr2rc402hML
		del cx
		dx := 0
		jmp _UWFWL7wtDIpLH8Uox@o2
:_UWFWL7wtDIpLH8Uox@o2
		jmp:neq!(dx, math:fac(999)) _h#Ikj#cdsKJsOVs4Bv9$
		jmp _w#HN3UMEDrsXYPLk$WNF
:_h#Ikj#cdsKJsOVs4Bv9$
		_printf <u16>'%d манул(а/ов)':fmt!(test_var)
		add! dx, 1
		jmp _UWFWL7wtDIpLH8Uox@o2
:_w#HN3UMEDrsXYPLk$WNF
		del dx
		wxA5CDPSnIG7xoj$tuJh := enumerate(L:get_states())
		ikV#PSQDKVIScC03fTeWe#i8 = 0
		jmp _Gi$96@2IKKDHmY3SpTam
:_Gi$96@2IKKDHmY3SpTam
		jmp:neq!(_ikV#PSQDKVIScC03fTeWe, wxA5CDPSnIG7xoj$tuJh:size()) _ZT9lioYPSeYnL5LRp1qa
		jmp _#eRLq2vhC$KmJyBPx$uC
:_ZT9lioYPSeYnL5LRp1qa
		(el1, el2) := wxA5CDPSnIG7xoj$tuJh[ikV#PSQDKVIScC03fTeWe]
		_printf <u16>'%s %s':fmt!(el1, el2)
		add! ikV#PSQDKVIScC03fTeWe, 1
		jmp _Gi$96@2IKKDHmY3SpTam
:_#eRLq2vhC$KmJyBPx$uC
		del (el1, el2)
		defun test, _test$ZQldNAiY@gu@#yKRUUwv
		nop!
:_test$ZQldNAiY@gu@#yKRUUwv
		(arg1#<member 'U8' of 'Type' objects>, arg2#<member 'U16' of 'Type' objects>) = ('test', 'тест')
		(arg1#<member 'U8' of 'Type' objects>, arg2#<member 'U16' of 'Type' objects>) = any!(%*) ?: %1..2
		_printf <u8>'test'
		jmp _test$MI1uzMBfE7QD#mBFIrWI
:_test$MI1uzMBfE7QD#mBFIrWI
