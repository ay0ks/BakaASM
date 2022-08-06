	_using $:enumerate
	_using $:lua
	_using $:sol
.data
		L := sol::state
		test_var := 10
.text
		L:open_lib(sol::lib::base, sol::lib::package)
		i := 0
		jmp _LCY3$Y@$liDyzT8#doXZd
:_LCY3$Y@$liDyzT8#doXZd
		jmp:neq!(i, math:fac(999)) _D3aJG9oj$EThQ8P7VOGc0
		jmp _5eIJVA4YsEmPjqsWBcUvg
:_D3aJG9oj$EThQ8P7VOGc0
		_printf <u8>'%d left':fmt!(test_var)
		add! i, 1
		jmp _LCY3$Y@$liDyzT8#doXZd
:_5eIJVA4YsEmPjqsWBcUvg
		del i
		cx := 0
		jmp _Y$#@Ev6E6pRFLZNNxt9cS
:_Y$#@Ev6E6pRFLZNNxt9cS
		jmp:neq!(cx, math:fac(999)) _8JJ5@2iRZ#BHy63dw@gPG
		jmp _eYcw$YDHVQWA#F@lNBQK1
:_8JJ5@2iRZ#BHy63dw@gPG
		_printf <u16>'%d манул':fmt!(test_var, (test_var:size(), leq! 4) ? 'а' : 'ов')
		add! cx, 1
		jmp _Y$#@Ev6E6pRFLZNNxt9cS
:_eYcw$YDHVQWA#F@lNBQK1
		del cx
		dx := 0
		jmp _BPI0l$2mcDVNseUXUTyZR
:_BPI0l$2mcDVNseUXUTyZR
		jmp:neq!(dx, math:fac(999)) _c$WxFhppJ$Ke5ysQn7bYR
		jmp _TWIFBOP$QC9u2erYCLb4L
:_c$WxFhppJ$Ke5ysQn7bYR
		_printf <u16>'%d манул(а/ов)':fmt!(test_var)
		add! dx, 1
		jmp _BPI0l$2mcDVNseUXUTyZR
:_TWIFBOP$QC9u2erYCLb4L
		del dx
		BBIzFzqCxIqR8AeSCrbRV := enumerate(L:get_states())
		i$$UzVR$XGejNpyd3oD@u$#i8 = 0
		jmp _HCeJ8AfKSifjeO#YXDv#X
:_HCeJ8AfKSifjeO#YXDv#X
		jmp:neq!(_i$$UzVR$XGejNpyd3oD@u$, BBIzFzqCxIqR8AeSCrbRV:size()) _VP$rWdSrBeNOEDed5rymc
		jmp _NjB@$B9CTZGSQjC#VXZlc
:_VP$rWdSrBeNOEDed5rymc
		(el1, el2) := BBIzFzqCxIqR8AeSCrbRV[i$$UzVR$XGejNpyd3oD@u$]
		_printf <u16>'%s %s':fmt!(el1, el2)
		add! i$$UzVR$XGejNpyd3oD@u$, 1
		jmp _HCeJ8AfKSifjeO#YXDv#X
:_NjB@$B9CTZGSQjC#VXZlc
		del (el1, el2)
		defun test, _test$#81D0mEiCM@36e8WMZ5Qo
		nop!
:_test$#81D0mEiCM@36e8WMZ5Qo
		(arg1#u8, arg2#u16) = ('test', 'тест')
		(arg1#u8, arg2#u16) = any!(%*) ?: %1..2
		_printf <u8>'test'
		jmp _test$9C$9xD$KoLd$iWWx#I3UI
:_test$9C$9xD$KoLd$iWWx#I3UI
