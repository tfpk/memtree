export class MemoryLocation {
  constructor(id: string, loc: any) {
    this.id = id;
    this.name = loc.name!;
    this.ctype = loc.ctype!;
    this.value = loc.value! as any;
    this.references = loc.references! as any;
    this.is_array = loc.type_bools!.is_array!;
    this.is_struct = loc.type_bools!.is_struct!;
  }
  
  id: string;
  name: string[];
  ctype: string;
  value: any;
  references: any;
  
  is_array: boolean;
  is_struct: boolean;
}
