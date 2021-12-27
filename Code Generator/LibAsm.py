class FuncAsm:
	StartProgr = ['assume cs:cod, ds:d, ss:s', 's segment stack', 'dw 128 dup (?)', 's ends']
	Variables = ['d segment']
	CodeVariable = []
	CodeMain = []
	CodeSeg = []
	marka = 0
	CodeProcedure = ['cod segment']
	NameProgramm = ''
	ProcTree = []
	EndProgram = ''
	EndVar = 'd ends'
	CodeEnd = []
	Code = []
	WriteLn = [
		"IntegerOut  proc",
		"pop ax",
		"xor cx,cx",
		"mov bx,10",
		"cmp ax,0",
		"jge m",
		"neg ax",
		"push ax",
		"mov ah,2",
		"mov dl,'-'",
		"int 21h",
		"pop ax",
		"m:  inc cx",
		"xor dx,dx",
		"div bx",
		"push dx",
		"or  ax,ax",
		"jnz m",
		"m1: pop dx",
		"add dx,'0'",
		"mov ah,2",
		"int 21h",
		"loop m1",
		"ret",
		"IntegerOut  endp"
		]
	def ProcBollean(self, Boolean, CodeAsm):
		if(Boolean['value']):
			Local_string = 'push 1'
			CodeAsm.append(Local_string)
			return
		else:
			Local_string = 'push 0'
			CodeAsm.append(Local_string)
			return

	def ProcOperator(self, Operator, CodeAsm):
#======================   U_MINUS   ==========================
		if(Operator['operator']=='u_minus'):
			Right = Operator['operandRight']
			if ((Right['type']=='variable') | (Right['type'] == 'number')):
				if(Right['type'] == 'variable'):
					Local_string = 'mov ax,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'neg ax'
				CodeAsm.append(Local_string)
				Local_string = 'push ax'
				CodeAsm.append(Local_string)
				return
			else:
				self.ProcOperator(Right, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'neg ax'
					CodeAsm.append(Local_string)
					Local_string = 'push ax'
					CodeAsm.append(Local_string)
					return
#======================   PLUS   =============================
		if(Operator['operator']=='plus'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'add ax,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'add ax,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'push ax'
				CodeAsm.append(Local_string)
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'add ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'push ax'
				CodeAsm.append(Local_string)
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov ax,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov ax,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'add ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'push ax'
					CodeAsm.append(Local_string)
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'add ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'push ax'
					CodeAsm.append(Local_string)
					return
#======================   MINUS ======= ======================
		if(Operator['operator']=='minus'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'sub ax,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'sub ax,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'push ax'
				CodeAsm.append(Local_string)
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'sub ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'push ax'
				CodeAsm.append(Local_string)
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'sub ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'push ax'
					CodeAsm.append(Local_string)
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'sub ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'push ax'
					CodeAsm.append(Local_string)
					return
#======================   MULTIPLY ===========================
		if(Operator['operator']=='multiply'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'imul ' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'imul' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'push ax'
				CodeAsm.append(Local_string)
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'imul bx'
				CodeAsm.append(Local_string)
				Local_string = 'push ax'
				CodeAsm.append(Local_string)
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'imul bx'
					CodeAsm.append(Local_string)
					Local_string = 'push ax'
					CodeAsm.append(Local_string)
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'imul bx'
					CodeAsm.append(Local_string)
					Local_string = 'push ax'
					CodeAsm.append(Local_string)
					return
#======================   DIV    =============================
		if((Operator['operator']=='div') | (Operator['operator']=='divide')):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'idiv' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'idiv' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'mov bx,al'
				CodeAsm.append(Local_string)
				Local_string = 'push bx'
				CodeAsm.append(Local_string)
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'idiv bx'
				CodeAsm.append(Local_string)
				Local_string = 'mov bx,al'
				CodeAsm.append(Local_string)
				Local_string = 'push bx'
				CodeAsm.append(Local_string)
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'idiv bx'
					CodeAsm.append(Local_string)
					Local_string = 'mov bx,al'
					CodeAsm.append(Local_string)
					Local_string = 'push bx'
					CodeAsm.append(Local_string)
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'idiv bx'
					CodeAsm.append(Local_string)
					Local_string = 'mov bx,al'
					CodeAsm.append(Local_string)
					Local_string = 'push bx'
					CodeAsm.append(Local_string)
					return
#======================   MOD    =============================
		if(Operator['operator']=='mod'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'idiv' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'idiv' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'mov bx,ah'
				CodeAsm.append(Local_string)
				Local_string = 'push bx'
				CodeAsm.append(Local_string)
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'idiv bx'
				CodeAsm.append(Local_string)
				Local_string = 'mov bx,ah'
				CodeAsm.append(Local_string)
				Local_string = 'push bx'
				CodeAsm.append(Local_string)
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'idiv bx'
					CodeAsm.append(Local_string)
					Local_string = 'mov bx,ah'
					CodeAsm.append(Local_string)
					Local_string = 'push bx'
					CodeAsm.append(Local_string)
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'idiv bx'
					CodeAsm.append(Local_string)
					Local_string = 'mov bx,ah'
					CodeAsm.append(Local_string)
					Local_string = 'push bx'
					CodeAsm.append(Local_string)
					return
#======================   LESS   =============================
		if(Operator['operator']=='less'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'mov bx,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov bx,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'push cf'
				CodeAsm.append(Local_string)
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'push cf'
				CodeAsm.append(Local_string)
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'push cf'
					CodeAsm.append(Local_string)
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'push cf'
					CodeAsm.append(Local_string)
					return
#======================   MORE    ============================
		if(Operator['operator']=='more'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'mov bx,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov bx,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'ja m' + str(self.marka)
				CodeAsm.append(Local_string)
				Local_string = 'push  0'
				CodeAsm.append(Local_string)
				Local_string = 'jmp m' + str(self.marka) + 'end'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + ': push 1'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + 'end: '
				CodeAsm.append(Local_string)
				self.marka = self.marka+1
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'ja m' + str(self.marka)
				CodeAsm.append(Local_string)
				Local_string = 'push  0'
				CodeAsm.append(Local_string)
				Local_string = 'jmp m' + str(self.marka) + 'end'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + ': push 1'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + 'end: '
				CodeAsm.append(Local_string)
				self.marka = self.marka+1
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'ja m' + str(self.marka)
					CodeAsm.append(Local_string)
					Local_string = 'push  0'
					CodeAsm.append(Local_string)
					Local_string = 'jmp m' + str(self.marka) + 'end'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + ': push 1'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + 'end: '
					CodeAsm.append(Local_string)
					self.marka = self.marka+1
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'ja m' + str(self.marka)
					CodeAsm.append(Local_string)
					Local_string = 'push  0'
					CodeAsm.append(Local_string)
					Local_string = 'jmp m' + str(self.marka) + 'end'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + ': push 1'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + 'end: '
					CodeAsm.append(Local_string)
					self.marka = self.marka+1
					return
#======================   EQUAL   ============================
		if(Operator['operator']=='equal'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'mov bx,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov bx,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'push zf'
				CodeAsm.append(Local_string)
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'push zf'
				CodeAsm.append(Local_string)
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'push zf'
					CodeAsm.append(Local_string)
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'push zf'
					CodeAsm.append(Local_string)
					return
#======================   NON-EQUAL    =======================
		if(Operator['operator']=='non-equal'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'mov bx,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov bx,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'jne m' + str(self.marka)
				CodeAsm.append(Local_string)
				Local_string = 'push  0'
				CodeAsm.append(Local_string)
				Local_string = 'jmp m' + str(self.marka) + 'end'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + ': push 1'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + 'end: '
				CodeAsm.append(Local_string)
				self.marka = self.marka+1
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'jne m' + str(self.marka)
				CodeAsm.append(Local_string)
				Local_string = 'push  0'
				CodeAsm.append(Local_string)
				Local_string = 'jmp m' + str(self.marka) + 'end'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + ': push 1'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + 'end: '
				CodeAsm.append(Local_string)
				self.marka = self.marka+1
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'jne m' + str(self.marka)
					CodeAsm.append(Local_string)
					Local_string = 'push  0'
					CodeAsm.append(Local_string)
					Local_string = 'jmp m' + str(self.marka) + 'end'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + ': push 1'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + 'end: '
					CodeAsm.append(Local_string)
					self.marka = self.marka+1
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'jne m' + str(self.marka)
					CodeAsm.append(Local_string)
					Local_string = 'push  0'
					CodeAsm.append(Local_string)
					Local_string = 'jmp m' + str(self.marka) + 'end'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + ': push 1'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + 'end: '
					CodeAsm.append(Local_string)
					self.marka = self.marka+1
					return
#======================   LESS-EQUAL    ======================
		if(Operator['operator']=='less-equal'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'mov bx,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov bx,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'jbe m' + str(self.marka)
				CodeAsm.append(Local_string)
				Local_string = 'push  0'
				CodeAsm.append(Local_string)
				Local_string = 'jmp m' + str(self.marka) + 'end'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + ': push 1'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + 'end: '
				CodeAsm.append(Local_string)
				self.marka = self.marka+1
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'jbe m' + str(self.marka)
				CodeAsm.append(Local_string)
				Local_string = 'push  0'
				CodeAsm.append(Local_string)
				Local_string = 'jmp m' + str(self.marka) + 'end'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + ': push 1'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + 'end: '
				CodeAsm.append(Local_string)
				self.marka = self.marka+1
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'jbe m' + str(self.marka)
					CodeAsm.append(Local_string)
					Local_string = 'push  0'
					CodeAsm.append(Local_string)
					Local_string = 'jmp m' + str(self.marka) + 'end'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + ': push 1'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + 'end: '
					CodeAsm.append(Local_string)
					self.marka = self.marka+1
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'jbe m' + str(self.marka)
					CodeAsm.append(Local_string)
					Local_string = 'push  0'
					CodeAsm.append(Local_string)
					Local_string = 'jmp m' + str(self.marka) + 'end'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + ': push 1'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + 'end: '
					CodeAsm.append(Local_string)
					self.marka = self.marka+1
					return
#======================   MORE-EQUAL    ======================
		if(Operator['operator']=='more-equal'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if(((Left['type']=='variable') | (Left['type'] == 'number')) & ((Right['type']=='variable') | (Right['type'] == 'number'))):
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				if(Right['type'] == 'variable'):
					Local_string = 'mov bx,' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov bx,' + str(Right['number'])
					CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'jae m' + str(self.marka)
				CodeAsm.append(Local_string)
				Local_string = 'push  0'
				CodeAsm.append(Local_string)
				Local_string = 'jmp m' + str(self.marka) + 'end'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + ': push 1'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + 'end: '
				CodeAsm.append(Local_string)
				self.marka = self.marka+1
				return
			if((Left['type'] == 'variable') | (Left['type'] == 'number')):
				self.ProcOperator(Right, CodeAsm)
				if(Left['type'] == 'variable'):
					Local_string = 'mov ax,' + Left['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'mov ax,' + str(Left['number'])
					CodeAsm.append(Local_string)
				Local_string = 'pop bx'
				CodeAsm.append(Local_string)
				Local_string = 'cmd ax,bx'
				CodeAsm.append(Local_string)
				Local_string = 'jae m' + str(self.marka)
				CodeAsm.append(Local_string)
				Local_string = 'push  0'
				CodeAsm.append(Local_string)
				Local_string = 'jmp m' + str(self.marka) + 'end'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + ': push 1'
				CodeAsm.append(Local_string)
				Local_string = 'm' + str(self.marka) + 'end: '
				CodeAsm.append(Local_string)
				self.marka = self.marka+1
				return
			else:
				self.ProcOperator(Left, CodeAsm)
				if((Right['type'] == 'variable') | (Right['type'] == 'number')):
					if(Right['type'] == 'variable'):
						Local_string = 'mov bx,' + Right['name']
						CodeAsm.append(Local_string)
					else:
						Local_string = 'mov bx,' + str(Right['number'])
						CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'jae m' + str(self.marka)
					CodeAsm.append(Local_string)
					Local_string = 'push  0'
					CodeAsm.append(Local_string)
					Local_string = 'jmp m' + str(self.marka) + 'end'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + ': push 1'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + 'end: '
					CodeAsm.append(Local_string)
					self.marka = self.marka+1
					return
				else:
					self.ProcOperator(Left, CodeAsm)
					self.ProcOperator(Right, CodeAsm)
					Local_string = 'pop bx'
					CodeAsm.append(Local_string)
					Local_string = 'pop ax'
					CodeAsm.append(Local_string)
					Local_string = 'cmd ax,bx'
					CodeAsm.append(Local_string)
					Local_string = 'jae m' + str(self.marka)
					CodeAsm.append(Local_string)
					Local_string = 'push  0'
					CodeAsm.append(Local_string)
					Local_string = 'jmp m' + str(self.marka) + 'end'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + ': push 1'
					CodeAsm.append(Local_string)
					Local_string = 'm' + str(self.marka) + 'end: '
					CodeAsm.append(Local_string)
					self.marka = self.marka+1
					return
#======================   AND   ======= ======================
		if(Operator['operator']=='and'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if((Left['type']=='boolean')  & (Right['type']=='boolean')):
				self.ProcBollean(Left, CodeAsm)
				self.ProcBollean(Right, CodeAsm)
			elif((Left['type']=='operator')  & (Right['type']=='operator')):
				self.ProcOperator(Left, CodeAsm)
				self.ProcOperator(Right, CodeAsm)
			Local_string = 'pop ax'
			CodeAsm.append(Local_string)
			Local_string = 'pop bx'
			CodeAsm.append(Local_string)
			Local_string = 'and ax,bx'
			CodeAsm.append(Local_string)
			Local_string = 'push ax'
			CodeAsm.append(Local_string)
#======================   OR    ==============================
		if(Operator['operator']=='or'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if((Left['type']=='boolean')  & (Right['type']=='boolean')):
				self.ProcBollean(Left, CodeAsm)
				self.ProcBollean(Right, CodeAsm)
			elif((Left['type']=='operator')  & (Right['type']=='operator')):
				self.ProcOperator(Left, CodeAsm)
				self.ProcOperator(Right, CodeAsm)
			Local_string = 'pop ax'
			CodeAsm.append(Local_string)
			Local_string = 'pop bx'
			CodeAsm.append(Local_string)
			Local_string = 'or ax,bx'
			CodeAsm.append(Local_string)
			Local_string = 'push ax'
			CodeAsm.append(Local_string)
#======================   ASSIGN    ==========================
		if(Operator['operator']=='assign'):
			Left = Operator['operandLeft']
			Right = Operator['operandRight']
			if((Right['type']=='number')|(Right['type']=='variable')):
				if(Right['type'] == 'variable'):
					Local_string = 'push ' + Right['name']
					CodeAsm.append(Local_string)
				else:
					Local_string = 'push ' + str(Right['number'])
					CodeAsm.append(Local_string)
			else:
				self.ProcOperator(Right, CodeAsm)
			Local_string = 'pop ax'
			CodeAsm.append(Local_string)
			Local_string = 'mov ' + Left['name'] + ',ax'
			CodeAsm.append(Local_string)

	def ProcVariable(self,CodeVariable, var, Variables):
		VarAsm = ''
		if(var['name']=='-'):
			self.NameProgramm = var['constValue'] + ':'
			self.EndProgram = 'end ' + self.NameProgramm
			self.CodeEnd = ['cod ends', self.EndProgram]
			return
		VarAsm = var['name'] + ' dw '
		if(var['constValue'] == None):
			VarAsm = VarAsm + '?'
		else:
			VarConstValue = var['constValue']
			if(VarConstValue['type'] == 'number'):
				VarAsm = VarAsm + str(VarConstValue['number'])
			else:
				VarAsm = VarAsm + '?'
				self.ProcOperator(VarConstValue, CodeVariable)
				Local_string = 'pop ax'
				CodeVariable.append(Local_string)
				Local_string = 'mov' + var['name'] + ',ax'
				CodeVariable.append(Local_string)
		Variables.append(VarAsm)

	def ProcWhile(self, OperWhile, CodeAsm):
		LocalMarka = self.marka
		self.marka = self.marka+1
		Local_string = 'lstart' + str(LocalMarka) + ':'
		CodeAsm.append(Local_string)
		MarkaEnd = 'lend' + str(LocalMarka) + ':'
		if(OperWhile['condition':'type']=='boolean'):
			self.ProcBollean(OperWhile['condition'], CodeAsm)
		else:
			self.ProcOperator(OperWhile['condition'], CodeAsm, self.marka)
		Local_string = 'pop ax' 
		CodeAsm.append(Local_string)
		Local_string = 'cmp ax,0'
		CodeAsm.append(Local_string)
		Local_string = 'je lend' + str(LocalMarka)
		CodeAsm.append(Local_string)

		self.ProcBody(CodeAsm, OperWhile['body'], MarkaEnd)

		Local_string = 'jmp mstart' + str(LocalMarka)
		CodeAsm.append(Local_string)
		Local_string = 'lend' + str(LocalMarka) + ':'
		CodeAsm.append(Local_string)
		return

	def ProcCall(self, OperCall, CodeAsm, MarkaEnd):
		if(OperCall['function']=='exit'):
			Local_string = 'jmp ' + MarkaEnd
			CodeAsm.append(Local_string)
			return
		elif(OperCall['function']=='writeln'):
			Local_string = 'push ax' 
			CodeAsm.append(Local_string)
			Local_string = 'call ' + OperCall['function']
			CodeAsm.append(Local_string)
			return

		for Func in self.ProcTree:
			if(OperCall['function']==Func['name']):
				LocalFuncArg = Func['arguments']

		SizeOperCall = len(OperCall['arguments'])
		for LocArg in OperCall['arguments']:
			if(LocArg['type']=='number'):
				Local_string = 'push ' + str(LocArg['number']) 
				CodeAsm.append(Local_string)
			elif(LocArg['type']=='variable'):
				Local_string = 'push ' + LocArg['name'] 
				CodeAsm.append(Local_string)
			else:
				self.ProcOperator(LocArg, CodeAsm, self.marka)
		
		Local_string = 'call ' + OperCall['function']
		CodeAsm.append(Local_string)
		LogArg = OperCall['arguments']
		for NumVar in range(OperCall['arguments']-1, 0, -1):
			Local_string = 'pop ax' 
			CodeAsm.append(Local_string)
			if(LocalFuncArg[NumVar['pointer']]):
				Local_string = 'mov ' + LogArg[NumVar['name']] + ',ax'
				CodeAsm.append(Local_string)
		return

	def ProcFor(self, OperFor, Code):
		LocalMarka = self.marka
		self.marka = self.marka + 1
		MarkaEnd ='lend' + str(LocalMarka) + ':' 
		From = OperFor['from']
		To = OperFor['to']
		if(From['type']=='number'):
			Local_string = 'push ' + str(From['number'])
			Code.append(Local_string)
		elif(From['type']=='variable'):
			Local_string = 'push ' + From['name'] 
			Code.append(Local_string)
		else:
			self.ProcOperator(From, Code, LocalMarka)
		Local_string = 'lstart' + str(LocalMarka) + ':'
		Code.append(Local_string)
		
		self.ProcBody(Code, OperFor['body'], MarkaEnd)

		if(To['type']=='number'):
			Local_string = 'push ' + str(To['number'])
			Code.append(Local_string)
		elif(To['type']=='variable'):
			Local_string = 'push ' + To['name'] 
			Code.append(Local_string)
		else:
			self.ProcOperator(To, Code, LocalMarka)
		Local_string = 'pop ax'
		Code.append(Local_string)
		Local_string = 'pop bx'
		Code.append(Local_string)
		Local_string = 'cmp ax, bx'
		Code.append(Local_string)
		if(OperFor['ascending']==True):
			Local_string = 'add bx,1'
			Code.append(Local_string)
		else:
			Local_string = 'sub bx,1'
			Code.append(Local_string)
			Local_string = 'push bx'
			Code.append(Local_string)
			Local_string = 'jhe lstart' + str(LocalMarka)
			Code.append(Local_string)
			Local_string = 'lend' + str(LocalMarka) + ':'
			Code.append(Local_string)
			Local_string = 'pop ax'
			Code.append(Local_string)
		return

	def ProcProcedure(self, CodeProcedure, Procedure):
		for LocProcedure in Procedure:
			self.ProcLocProcedure(CodeProcedure, LocProcedure)
		return

	def ProcLocProcedure(self, CodeProcedure, LocProcedure):
		LocNumArg = len(LocProcedure['arguments'])
		LocNumArg = LocNumArg*2
		for LocVar in LocProcedure['arguments']:
			Local_string = '[bp+' + str(LocNumArg) + ']' 
			LocVar['name'] = Local_string
			LocNumArg = LocNumArg - 2
		LocNumVar = len(LocProcedure['variables'])
		LocNumVar = LocNumVar*2
		for LocVar in LocProcedure['variables']:
			Local_string = '[bp-' + str(LocNumVar) + ']' 
			LocVar['name'] = Local_string
			LocNumVar = LocNumVar - 2
		Local_string = LocProcedure['name'] + ' proc'
		CodeProcedure.append(Local_string)
		Local_string = 'push bp'
		CodeProcedure.append(Local_string)
		Local_string = 'mov bp, sp'
		CodeProcedure.append(Local_string)

		Local_string = 'mov ax,0'
		CodeProcedure.append(Local_string)
		LocNumVar = len(LocProcedure['variables'])
		for LocVar in LocProcedure['variables']:
			if(LocVar['constValue']==None):
				Local_string = 'push ax'
				CodeProcedure.append(Local_string)
			else:
				LocLocVar = LocVar['constvalue']
				if(LocLocVar['type']=='number'):
					Local_string = 'push ' + str(LocLocVar['number'])
					CodeProcedure.append(Local_string)
				else:
					self.ProcOperator(LocLocVar, CodeProcedure, self.marka)

		self.ProcBody(CodeProcedure, LocProcedure['body'], None)
		LocNumVar = len(LocProcedure['variables'])
		for i in range(LocNumVar):
			Local_string = 'pop ax'
			CodeProcedure.append(Local_string)
		Local_string = 'pop bp'
		CodeProcedure.append(Local_string)
		Local_string = 'ret'
		CodeProcedure.append(Local_string)
		Local_string = LocProcedure['name'] + ' endp'
		CodeProcedure.append(Local_string)


	def ProcBody(self, Code, Body, MarkaEnd):
		for LocOper in Body:
			if(LocOper['type']=='call'):
				self.ProcCall(LocOper, Code, MarkaEnd)
			elif(LocOper['type']=='operator'):
				self.ProcOperator(LocOper, Code)
			elif(LocOper['type']=='for'):
				self.ProcFor(LocOper, Code)
			elif(LocOper['type']=='while'):
				self.ProcWhile(LocOper, Code)
			return