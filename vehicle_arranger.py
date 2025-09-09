import os
import sys


# read argv
args = sys.argv

# UI function
# on going...
def UI_function():
    where_show=0
    print_function("What is the input file name?",where_show)
    infile_path=input_function()
    print_function("What is the output file name?",where_show)
    outfile_path=input_function()
    return infile_path,outfile_path,where_show




# main: only read args
def main():
    if len(args)>2:
        infile_path=args[1]
        outfile_path=args[2]
        where_show=0
    elif len(args)==2:
        infile_path=args[1]
        outfile_path=args[1]
        where_show=0
    else:
        infile_path,outfile_path,where_show=UI_function()
    vehicle_arrange(infile_path,outfile_path,where_show)




# input function

def input_function(input_file="",input_way="",where_show=0):
    if where_show==1:
        input_file=""
    else:
        return input()

        





# print function
def print_function(texts,where_show=0):
    if where_show!=1:
        print(texts+"\n")

def ask_function(texts,answer,where_show=0,output_type=0):
    print_function(texts+"(default:"+str(answer)+")",where_show)
    output=input_function(where_show=where_show)
    # output_type is int_value. output_type==0 means output must be str. output_type==1 means output must be int.
    if output == "":
        print_function("No input. Treated as "+str(answer))
        output=answer
    if output_type==1:
        try:
            return int(output)
        except Exception:
            print_function("input is not int. Trated as "+str(answer))
    else:
        return output

# main_function
def vehicle_arrange(infile_path,outfile_path,where_show=0):
    climate_list=["water", "desert", "tropic", "mediterran", "temperate", "tundra", "rocky", "arctic"]
    def byte_to_date(inbyte,version=1):
        indate=int.from_bytes(inbyte,byteorder="little")
        if version==0:
            indata=indata//16*12+indata%16
        year=indate//12
        date=indate%12+1
        return year,date
    def date_to_byte(year,date,version=1):
        if version==1:
            temp_date=year*12+date-1
        if version==0:
            temp_date=year*16+date-1
        return temp_date.to_bytes(2,byteorder="little")
    def int_to_climates(input):
        return_list=[]
        for i in range(len(climate_list)):
            climate_void=(input & 2**i)>>i
            if climate_void==1:
                return_list.append(climate_list[i])
        return return_list
    def climates_to_int(input_list):
        return_int=0
        for i in range(len(climate_list)):
            for j in (input_list):
                if climate_list[i]==j:
                    return_int+=2**i
        return return_int
    def climate_changing(input_int,where_show):
        continue_flag=1
        return_int=input_int
        temp_climate_list=int_to_climates(input_int)
        while continue_flag==1:
            print_function("Allowed Climate List:",where_show)
            for i in range(len(temp_climate_list)):
                print_function(str(i)+":"+str(temp_climate_list[i]),where_show)
            print_function("-------------------",where_show)
            print_function("Do you want to change allowed climate? Please select changing way.",where_show)
            print_function("1.Remove an Allowed Climate",where_show)
            print_function("2.Add an Allowed Climate",where_show)
            print_function("x.Exit (Not Change)",where_show)
            choice=input_function(where_show=where_show)
            if str(choice)=="1":
                print_function("-------------------",where_show)
                print_function("Which one do you want to remove? Select number.",where_show)
                for i in range(len(temp_climate_list)):
                    print_function(str(i)+":"+str(temp_climate_list[i]),where_show)
                print_function("x:Exit",where_show)
                remove_choice=input_function(where_show=where_show)
                for i in range(len(temp_climate_list)):
                    if str(remove_choice)==str(i): 
                        temp_climate_list.pop(i)
                        print_function("remove "+str(temp_climate_list[i]),where_show)
            elif str(choice)=="2":
                print_function("-------------------",where_show)
                print_function("Which one do you want to add? Select number.",where_show)
                for i in range(len(climate_list)):
                    print_function(str(i)+":"+str(climate_list[i]),where_show)
                print_function("x:Exit",where_show)
                add_choice=input_function(where_show=where_show)
                for i in range(len(temp_climate_list)):
                    if str(add_choice)==str(i): 
                        if climate_list[i] in temp_climate_list:
                            print_function("Already added"+str(climate_list[i]),where_show)
                        else:
                            climate_list.append(str(climate_list[i]))    
                            print_function("add "+str(climate_list[i]),where_show)
            else:
                print_function("End changing allowed climate.",where_show)
                continue_flag=0
        return_int=climates_to_int(temp_climate_list)
        return return_int
    def copy_header(infile,outfile):
        # copy file header 
        for i in range(1000):
            temp_data=infile.read(1)
            outfile.write(temp_data)
            if not temp_data:
                print_function("Is this a wrong file?",where_show)
                return False
            if temp_data==b"\x1a":
                version_data=infile.read(4)
                outfile.write(version_data)               
                return True
    def copy_root(infile,outfile):
        # copy root and read the number of addons in the pakfile
        root = infile.read(4)
        if root!=b"ROOT":
            print_function("Broken file",where_show)
            return False
        nchild_byte = infile.read(2)
        nchild = int.from_bytes(nchild_byte,byteorder="little")
        print_function("Number of addons : "+str(nchild),where_show)
        root_size = infile.read(2)
        outfile.write(root)
        outfile.write(nchild_byte)
        outfile.write(root_size)
        if nchild>0:
            copy_object(infile,outfile,nchild)
            return True
        else:
            print_function("a number of child is wrong",where_show)
            return False
    def copy_object(infile,outfile,root_nchild,holdflag=0,bytes=b"",need_return=0):
        for i in range(root_nchild):
            obj_type = infile.read(4)
            obj_nchild_byte = infile.read(2)
            obj_size_byte = infile.read(2)
            obj_nchild = int.from_bytes(obj_nchild_byte,byteorder="little")
            if obj_type == b"VHCL":
                outfile.write(obj_type)
                obj_size=int.from_bytes(obj_size_byte,byteorder="little")
                a=vehicle_arranging(infile,outfile,obj_nchild,obj_size)
                if not a:
                    break
            elif obj_type == b"BUIL":
                obj_size=int.from_bytes(obj_size_byte,byteorder="little")
                if(holdflag!=1):
                    outfile.write(obj_type)
                else:
                    bytes+=obj_type
                bytes+=building_arranging(infile,outfile,obj_nchild,obj_size,holdflag)
            elif obj_type == b"FACT":
                obj_size=int.from_bytes(obj_size_byte,byteorder="little")
                outfile.write(obj_type)
                a=factory_arranging(infile,outfile,obj_nchild,obj_size)
                if not a:
                    break
            else:
                if holdflag!=1:
                    outfile.write(obj_type)
                    outfile.write(obj_nchild_byte)
                    outfile.write(obj_size_byte)
                else:
                    bytes+=(obj_type+obj_nchild_byte+obj_size_byte)
                if obj_size_byte == b"\xFFFF":
                    obj_size_byte32 = infile.read(4)
                    if holdflag!=1:
                        outfile.write(obj_size_byte32)
                    else:
                        bytes+=(obj_size_byte32)
                    obj_size = int.from_bytes(obj_size_byte32,byteorder="little")
                else:
                    obj_size = int.from_bytes(obj_size_byte,byteorder="little")
                    copy_data = infile.read(obj_size)
                    if holdflag!=1:
                        outfile.write(copy_data)
                    else:
                        bytes+=copy_data
                bytes+=copy_object(infile,outfile,obj_nchild,holdflag,bytes=b"")
        if holdflag==1:
            return bytes
    def copy_node(infile,node):
        temp_node=infile.read(node)
        return temp_node
    def Remove_None(list):
        output=[]
        for i in range(len(list)):
            if str(list[i])!="none" or list[i]==b"\x00":
                output.append(list[i])
            # print(output)
        return output
    def Remove_Selected(list,removelist):
        output=[]
        for i in range(len(list)):
            flag = 0
            for j in range(len(removelist)):
                if i == removelist[j]:
                    flag = 1
            if flag == 0:
                output.append(list[i])
        return output
    def connecting_changing(connecting_list,l_or_r="leader"):
        print_function(l_or_r+" list",where_show)
        print_function("list length:"+str(len(connecting_list)),where_show)
        print_function("number\tname",where_show)
        for i in range(len(connecting_list)):
            print_function(str(i)+"\t"+str(connecting_list[i]),where_show)
        print_function("How to change? Please choose and input the number",where_show)
        print_function("  1.Remove None",where_show)
        print_function("  2.Remove restriction",where_show)
        print_function("  3.Add new connect permition",where_show)
        print_function("  4.Remove selected connect permition",where_show)
        print_function("  x.Exit",where_show)
        choice=input_function(where_show=where_show)
        if choice =="1":
            connecting_list=Remove_None(connecting_list)
            return connecting_changing(connecting_list,l_or_r)
        elif choice =="2":
            connecting_list=[]
            return connecting_changing(connecting_list,l_or_r)
        elif choice =="3":
            print_function("  what name?")
            temp_input=input_function(where_show=where_show)
            connecting_list.append(temp_input)
            return connecting_changing(connecting_list,l_or_r)
        elif choice=="4":
            print_function("  which one do you want to remove?")
            temp_input_int=input_function(where_show=where_show)
            try:
                temp_int=int(temp_input_int)
                connecting_list=Remove_Selected(connecting_list,[temp_int])
                return connecting_changing(connecting_list,l_or_r)
            except Exception:
                print_function("  wrong input")
                return connecting_changing(connecting_list,l_or_r)
        elif choice=="x":
            return connecting_list
        else:
            print_function("  wrong input")
            return connecting_changing(connecting_list,l_or_r)
    def read_xref(infile,type=b"VHCL"):
        xref=infile.read(4)
        xref_nchild=infile.read(2)
        xref_size_byte=infile.read(2)
        xref_size=int.from_bytes(xref_size_byte,byteorder="little")
        VHCL=infile.read(4)
        cflag=infile.read(1)
        output=infile.read(xref_size-6)
        infile.read(1)
        if xref==b"XREF" and xref_nchild==b"\x00\x00" and VHCL==type and (cflag==b"\x00"or cflag==b"\x01"):
            return output.decode("utf-8")
    def write_xref(outfile,text,type=b"VHCL",holdflag=0,fatal_flag=0):
        write_txt=b""
        write_txt+=(b"XREF")
        write_txt+=(b"\x00\x00")#must be a child
        size_int=4+1+len(text)+1
        write_txt+=(size_int.to_bytes(2,byteorder="little"))
        write_txt+=(type)
        write_txt+=(fatal_flag.to_bytes(1,byteorder="little"))#Fatal-Flag
        write_txt+=(text.encode("utf-8"))
        write_txt+=(b"\x00")
        if(holdflag!=1):
            outfile.write(write_txt)
        else:
            return write_txt
    def read_text(infile):
        text=infile.read(4)
        text_nchild=infile.read(2)
        text_size_byte=infile.read(2)
        text_size=int.from_bytes(text_size_byte,byteorder="little")
        output=infile.read(text_size-1)
        infile.read(1)
        if text==b"TEXT" and text_nchild==b"\x00\x00":
            return output.decode("utf-8")
    def write_text(outfile,text,holdflag=0):
        write_txt=b""
        write_txt+=(b"TEXT")
        write_txt+=(b"\x00\x00")#must be a child
        size_int=len(text)+1
        write_txt+=(size_int.to_bytes(2,byteorder="little"))
        write_txt+=(text.encode("utf-8"))
        write_txt+=(b"\x00")
        if(holdflag!=1):
            outfile.write(write_txt)
        else:
            return write_txt
    def vehicle_arranging(infile,outfile,obj_nchild,obj_size):
        temp_headnode=b""
        temp_obj_size=obj_size
        new_obj_size=0
        # copy and arrange setting of vehicle
        # version
        version_byte=copy_node(infile,2)
        version_int=int.from_bytes(version_byte,byteorder="little")
        if version_int & 0x8000:
            version=version_int&0x7FFF
        else:
            version=0
        # pakfile version changing
        if version>0:
            ask_version=ask_function("Do you want to change pak version to 0x800C? yes=1,no=other","1",where_show,0)
        if ask_version=="1":
            print_function("change version",where_show)
            new_version=0x800c
            write_version=new_version&0x7FFF
        else:
            print_function("NOT change version",where_show)
            new_version=version|0x8000
            write_version=version
        temp_obj_size-=2
        if version<=0:
            # we cannot treat too old version
            print_function("Too old",where_show)
            return False
        # cost
        if version < 12:
            price_byte32 = infile.read(4)
            price = int.from_bytes(price_byte32,byteorder="little")
            temp_obj_size-=4
        else:
            price_byte64 = infile.read(8)
            price = int.from_bytes(price_byte64,byteorder="little")
            temp_obj_size-=8            
        # capacity
        capacity_byte = infile.read(2)
        capacity = int.from_bytes(capacity_byte,byteorder="little")
        temp_obj_size-=2
        # loading_time
        if version>8:
            # depends on the version
            l_time_byte = infile.read(2)
            temp_obj_size-=2
            l_time = int.from_bytes(l_time_byte,byteorder="little")
        else:
            l_time = 1000
        # speed
        speed_byte = infile.read(2)
        speed_int = int.from_bytes(speed_byte,byteorder="little")
        temp_obj_size-=2
        # weight
        if version>9:
            weight_byte32 = infile.read(4)
            temp_obj_size-=4
            weight = int.from_bytes(weight_byte32,byteorder="little")
        else:
            weight_byte32 = infile.read(2)
            weight = int.from_bytes(weight_byte32,byteorder="little")
            if write_version>9:
                weight = weight*1000
            temp_obj_size-=2
        # axle_load
        if version>8:
            axle_byte=infile.read(2)
            axle_int=int.from_bytes(axle_byte,byteorder="little")
            temp_obj_size-=2
        else:
            axle_int=0
        # power
        if version>5:
            power_byte32 = infile.read(4)
            temp_obj_size-=4
        else:
            power_byte32 = infile.read(2)
            temp_obj_size-=2
        power = int.from_bytes(power_byte32,byteorder="little")
        # running cost
        if version<12:
            rcost_byte = infile.read(2)
            rcost = int.from_bytes(rcost_byte,byteorder="little")
            temp_obj_size-=2
        else:
            rcost_byte = infile.read(8)
            rcost = int.from_bytes(rcost_byte,byteorder="little")
            temp_obj_size-=8
        # monthly maintenance
        # depends on the version
        if version >8:
            if version > 11:
                mcost_byte32 = infile.read(8)
                temp_obj_size-=8
            elif version>10:
                mcost_byte32 = infile.read(4)
                temp_obj_size-=4
            else:
                mcost_byte32 = infile.read(2)
                temp_obj_size-=2
            mcost = int.from_bytes(mcost_byte32,byteorder="little")
        else:
            mcost = 0
        # Intro year
        intro_byte = infile.read(2)
        temp_obj_size-=2
        if version<5:
            intro_y,intro_m = byte_to_date(intro_byte,version=0)
        else:
            intro_y,intro_m = byte_to_date(intro_byte)
        # Retire year
        if version>2:
            retire_byte = infile.read(2)
            temp_obj_size-=2
            if version<5:
                retire_y,retire_m = byte_to_date(retire_byte,version=0)
            else:
                retire_y,retire_m = byte_to_date(retire_byte)
        else:
            retire_y,retire_m=2999,1
        # Engine gear
        if version>5:
            gear_byte=infile.read(2)
            temp_obj_size-=2
        else:
            gear_byte=infile.read(1)
            temp_obj_size-=1
        gear_int=int.from_bytes(gear_byte,byteorder="little")
        # waytype
        waytype_node+=copy_node(infile,1)
        temp_obj_size-=1
        # sound id
        soundid_node+=copy_node(infile,1)
        temp_obj_size-=1
        # engine type
        enginetype_node+=copy_node(infile,1)
        temp_obj_size-=1
        # length
        if version>6:
            vlength_byte=infile.read(1)
            vlength_int=int.from_bytes(vlength_byte,byteorder="little")
            temp_obj_size-=1
        else:
            vlength_int=8

        
        # leader reading
        leader_byte=infile.read(1)
        leader=int.from_bytes(leader_byte,byteorder="little")
        temp_obj_size-=1
        # trailer reading
        trailer_byte=infile.read(1)
        trailer=int.from_bytes(trailer_byte,byteorder="little")
        temp_obj_size-=1
        # freight image number (only for version updating)
        others_byte=b""
        if version<8 and write_version>7:
            freight_image_number_int=0
            others_byte+=freight_image_number_int.to_bytes(1,byteorder="little")
            new_obj_size+=1
        # other_params_reading
        others_byte+=infile.read(temp_obj_size)
        new_obj_size+=temp_obj_size
        temp_obj_size=0
        # get name
        name = read_text(infile)
        # other bytes: copyright, images etc.
        other_object += copy_object(infile,outfile,5,holdflag=1,bytes=b"",need_return=1)
        # leader and trailer reading
        temp_leaders=[]
        temp_trailers=[]
        for i in range(leader):
            temp_leaders.append(read_xref(infile))
        for i in range(trailer):
            temp_trailers.append(read_xref(infile))
        # now ask to write
        # show and ask name change
        name = ask_function("Name = "+str(name),name,where_show,0)
        # version
        temp_headnode+=new_version.to_bytes(2,byteorder="little")
        new_obj_size+=2
        # cost
        price = ask_function("cost = "+str(price),price,where_show,1)
        if(write_version<12):
            temp_headnode+=(price.to_bytes(4,byteorder="little"))
            new_obj_size+=4
        else:
            temp_headnode+=(price.to_bytes(8,byteorder="little"))
            new_obj_size+=8
        # capacity
        capacity = ask_function("capacity = "+str(capacity),capacity,where_show,1)
        temp_headnode+=(capacity.to_bytes(2,byteorder="little"))
        new_obj_size+=2
        # loading time
        if write_version>8:
            l_time = ask_function("loading time = "+str(l_time),l_time,where_show,1)
            temp_headnode+=(l_time.to_bytes(2,byteorder="little"))
            new_obj_size+=2
        # speed
        speed_int = ask_function("top speed = "+str(speed_int),speed_int,where_show,1)
        temp_headnode+=(speed_int.to_bytes(2,byteorder="little"))
        new_obj_size+=2
        # weight
        weight = ask_function("weight = "+str(weight),weight,where_show,1)
        if write_version>9:
            temp_headnode+=(weight.to_bytes(4,byteorder="little"))
            new_obj_size+=4
        else:
            temp_headnode+=(weight.to_bytes(2,byteorder="little"))
            new_obj_size+=2
        # axle_load
        if write_version>8:
            axle_int=ask_function("axle_load="+str(axle_int),axle_int,where_show,1)
            temp_headnode+=(axle_int.to_bytes(2,byteorder="little"))
            new_obj_size+=2 
        # power
        power = ask_function("power = "+str(power)+"kW",power,where_show,1)
        if write_version>5:
            temp_headnode+=(power.to_bytes(4,byteorder="little"))
            new_obj_size+=4
        else:
            temp_headnode+=(power.to_bytes(2,byteorder="little"))
            new_obj_size+=2
        # runnin const
        rcost = ask_function("running cost = "+str(rcost),rcost,where_show,1)
        if write_version<12:
            temp_headnode+=(rcost.to_bytes(2,byteorder="little"))
            new_obj_size+=2
        else:
            temp_headnode+=(rcost.to_bytes(8,byteorder="little"))
            new_obj_size+=8
        # monthly maintainance
        if write_version>8:
            mcost = ask_function("mcost = "+str(mcost),mcost,where_show,1)
            if write_version>10:
                temp_headnode+=(mcost.to_bytes(4,byteorder="little"))
                new_obj_size+=4
            else:
                temp_headnode+=(mcost.to_bytes(2,byteorder="little"))
                new_obj_size+=2
        # intro year
        intro_y = ask_function("intro_year :"+str(intro_y),intro_y,where_show,1)
        intro_m = ask_function("intro_month:"+str(intro_m),intro_m,where_show,1)
        if write_version<5:
            temp_headnode+=(date_to_byte(intro_y,intro_m,version=0))
        else:
            temp_headnode+=(date_to_byte(intro_y,intro_m))
        new_obj_size+=2
        # engine gear
        if write_version>5:
            temp_headnode+=(gear_int.to_bytes(2,byteorder="little"))
            new_obj_size+=2
        else:
            temp_headnode+=(gear_int.to_bytes(1,byteorder="little"))
            new_obj_size+=1
        # retire year
        if write_version>2:
            retire_y = ask_function("retire_year :"+str(retire_y),retire_y,where_show,1)
            retire_m = ask_function("retire_month:"+str(retire_m),retire_m,where_show,1)
            if write_version<5:
                temp_headnode+=(date_to_byte(retire_y,retire_m,version=0))
            else:
                temp_headnode+=(date_to_byte(retire_y,retire_m))
            new_obj_size+=2
        # waytype_node
        temp_headnode+=waytype_node
        new_obj_size+=1
        # sound id
        temp_headnode+=soundid_node
        new_obj_size+=1
        # engine type
        temp_headnode+=enginetype_node
        # length
        vlength_int = ask_function("mcost = "+str(vlength_int),vlength_int,where_show,1)
        if write_version>6:
            temp_headnode+=(vlength_int.to_bytes(1,byteorder="little"))
            new_obj_size+=1
        # leader and trailer changing
        result_leader_list=connecting_changing(temp_leaders,"leader")
        new_obj_size+=1
        result_trailer_list=connecting_changing(temp_trailers,l_or_r= "trailer")
        new_obj_size+=1
        new_node=obj_nchild-leader-trailer+len(result_leader_list)+len(result_trailer_list)
        # new node writing
        outfile.write(new_node.to_bytes(2,byteorder="little"))
        outfile.write(new_obj_size.to_bytes(2,byteorder="little"))
        outfile.write(temp_headnode)
        outfile.write(len(result_leader_list).to_bytes(1,byteorder="little"))
        outfile.write(len(result_trailer_list).to_bytes(1,byteorder="little"))
        outfile.write(others_byte)
        write_text(outfile,name)
        outfile.write(other_object)
        # write new leader list
        for i in range(len(result_leader_list)):
            write_xref(outfile,result_leader_list[i])
        for j in range(len(result_trailer_list)):
            write_xref(outfile,result_trailer_list[j])
        # write another nodes
        ANOTHERS = obj_nchild-6-leader-trailer
        if ANOTHERS>0:
            copy_object(infile,outfile,ANOTHERS,holdflag=0)
        return True
    def change_enable_goodstype(input_int,where_show):
        continue_flag=1
        return_int=input_int
        enable_goodstype_list=["passagiere","post","ware"]
        while continue_flag==1:
            print_function("Enable goods list:",where_show)
            for i in range(len(enable_goodstype_list)):
                if((return_int>>(i))&1>0):
                    print_function(str(i)+":"+str(enable_goodstype_list[i]),where_show)
            print_function("-------------------",where_show)
            print_function("Do you want to change allowed climate? Please select changing way.",where_show)
            print_function("1.Remove an Allowed Climate",where_show)
            print_function("2.Add an Allowed Climate",where_show)
            print_function("x.Exit (Not Change)",where_show)
            choice=input_function(where_show=where_show)
            if str(choice)=="1":
                print_function("-------------------",where_show)
                print_function("Which one do you want to remove? Select number.",where_show)
                for i in range(len(enable_goodstype_list)):
                    print_function(str(i)+":"+str(enable_goodstype_list[i]),where_show)
                remove_choice=input_function(where_show=where_show)
                try:
                    remove_choice_int=int(remove_choice)
                    if( 1<<(remove_choice_int)&return_int>0 ):
                        return_int-(1<<(remove_choice_int))
                except:
                    print_function("invalid entry",where_show)                    
            elif str(choice)=="2":
                print_function("-------------------",where_show)
                print_function("Which one do you want to remove? Select number.",where_show)
                for i in range(len(enable_goodstype_list)):
                    print_function(str(i)+":"+str(enable_goodstype_list[i]),where_show)
                remove_choice=input_function(where_show=where_show)
                try:
                    remove_choice_int=int(remove_choice)
                    if( (0<=remove_choice_int<3) and 1<<(remove_choice_int)&return_int==0 ):
                        return_int+(1<<(remove_choice_int))
                except:
                    print_function("invalid entry",where_show)                    
            else:
                print_function("End changing allowed climate.",where_show)
                continue_flag=0
        return return_int

    def building_arranging(infile,outfile,obj_nchild,obj_size,holdflags=0):
        btype_tuple=(
            "unknown",#0
            "attraction_city",#1
            "attraction_land",#2
            "monument",#3
            "factory",#4
            "townhall",#5
            "others",#6
            "headquarters",#7
            "bahnhof",#8,old_building_types : generic_stop, waytype=track
            "bushalt",#9,old_building_types : generic_stop, waytype=road
            "ladebucht",#10,old_building_types : generic_stop, waytype=road
            "dock",#11
            "binnenhafen",#12,old_building_types : generic_stop, waytype=water
            "airport",#13,old_building_types : generic_stop, waytype=air
            "monorailstop",#14,old_building_types : generic_stop, waytype = monorail
            "",#15 is empty
            "bahnhof_geb",#16,old_building_types : generic_extension, waytype=track
            "bushalt_geb",#17,old_building_types : generic_extension, waytype=road
            "ladebucht_geb",#18,old_building_types : generic_extension, waytype=road
            "hagen_geb",#19,old_building_types : generic_extension, waytype=water
            "binnenhafen_geb",#20,old_building_types : generic_extension, waytype = water
            "airport_geb",#21,old_building_types : generic_extension, waytype=air
            "monorail_geb",#22,old_building_types : generic_extension, waytype = monorail
            "",#23 is empty
            "",#24 is empty
            "",#25 is empty
            "",#26 is empty
            "",#27 is empty
            "",#28 is empty
            "",#29 is empty
            "wartehalle",#30,old_building_types : generic_extension, waytype = none
            "mail",#31,old_building_types : generic_extension, waytype = none
            "lagerhalle",#32,old_building_types : generic_extension, waytype = none
            "depot",#33
            "generic_stop",#34
            "generic_extension",#35
            "flat_dock",#36
            "city_res",#37
            "city_com",#38
            "city_ind"#39
        )
        old_btype_tuple=(
            "wohnung",
            "gewerbe",
            "industrie",
            "unknown"
        )
            
                
        temp_headnode=b""
        temp_obj_size=obj_size
        new_obj_size=0
        # copy and arrange setting of vehicle
        # version
        version_byte=copy_node(infile,2)
        version_int=int.from_bytes(version_byte,byteorder="little")
        if version_int & 0x8000:
            version=version_int&0x7FFF
        else:
            version=0
        # pakfile version changing
        if version>0:
            ask_version=ask_function("Do you want to change pak version to 0x800B? yes=1,no=other","1",where_show,0)
        if ask_version=="1":
            print_function("change version",where_show)
            new_version=0x800b
            write_version=new_version&0x7FFF
        else:
            print_function("NOT change version",where_show)
            new_version=version_int
            write_version=version
        temp_headnode+=new_version.to_bytes(2,byteorder="little")
        temp_obj_size-=2
        new_obj_size+=2  
        if version<0:
            return False
        else:
            old_btype_byte=infile.read(1)
            btype_byte=infile.read(1)
            temp_obj_size-=2
            old_btype_int=int.from_bytes(old_btype_byte,byteorder="little")
            btype_int=int.from_bytes(btype_byte,byteorder="little")
            level_byte=infile.read(2)
            temp_obj_size-=2
            level_int=int.from_bytes(level_byte,byteorder="little")+1
            extra_data_byte=infile.read(4)
            temp_obj_size-=4
            extra_data=int.from_bytes(extra_data_byte,byteorder="little")
            size_x_byte=infile.read(2)
            temp_obj_size-=2
            size_y_byte=infile.read(2)
            temp_obj_size-=2
            layout_byte=infile.read(1)
            temp_obj_size-=1
            size_x_int=int.from_bytes(size_x_byte,byteorder="little")
            size_y_int=int.from_bytes(size_y_byte,byteorder="little")
            layout_int=int.from_bytes(layout_byte,byteorder="little")
            if version>3:
                allowed_climates_byte=infile.read(2)
                temp_obj_size-=2
                allowed_climates_int=int.from_bytes(allowed_climates_byte,byteorder="little")
            else:
                allowed_climates_int=0x00FE
            if version> 2:
                enables_byte=infile.read(1)
                temp_obj_size-=1
                enables_int=int.from_bytes(enables_byte,byteorder="little")
            else:
                enables_int=0x80
            build_flag_byte=infile.read(1)
            temp_obj_size-=1
            build_flag_int=int.from_bytes(build_flag_byte,byteorder="little")
            # distribution weight
            build_chance_byte=infile.read(1)
            temp_obj_size-=1
            build_chance_int=int.from_bytes(build_chance_byte,byteorder="little")
            # intro and retire date
            if version>1:
                intro_byte=infile.read(2)
                retire_byte=infile.read(2)
                temp_obj_size-=4
                intro_y,intro_m=byte_to_date(intro_byte)
                retire_y,retire_m=byte_to_date(retire_byte)
            else:
                intro_y=1900
                intro_m=1
                retire_y=2999
                retire_m=1
            # animation frame per ms
            if version>4:
                animation_time_byte=infile.read(2)
                temp_obj_size-=2
                animation_time=int.from_bytes(animation_time_byte,byteorder="little")
            else:
                animation_time=300
            # capacity, maintenance cost, price
            if version>7:
                capacity_byte=infile.read(2)
                temp_obj_size-=2
                capacity_int=int.from_bytes(capacity_byte,byteorder="little")
                if version<11:
                    maintenance_byte=infile.read(4)
                    temp_obj_size-=4
                    maintenance_int=int.from_bytes(maintenance_byte,byteorder="little")
                    price_byte=infile.read(4)
                    temp_obj_size-=4
                    price_int=int.from_bytes(price_byte,byteorder="little")
                else:
                    maintenance_byte=infile.read(8)
                    temp_obj_size-=8
                    maintenance_int=int.from_bytes(maintenance_byte,byteorder="little")
                    price_byte=infile.read(8)
                    temp_obj_size-=8
                    price_int=int.from_bytes(price_byte,byteorder="little")
            else:
                capacity_int=level_int*32
                maintenance_int=level_int*100
                price_int=level_int*1000
            # allow underground
            if version>6:
                allow_underground_byte=infile.read(1)
                temp_obj_size-=1
                allow_underground_int=int.from_bytes(allow_underground_byte,byteorder="little")
            else:
                allow_underground_int=255
            # preservation year month
            if version>9:
                preservation_ym_byte=infile.read(2)
                temp_obj_size-=2
                preservation_y,preservation_m=byte_to_date(preservation_ym_byte)
            else:
                preservation_y=retire_y
                preservation_m=retire_m 
            # get building name
            name = read_text(infile)               
            #
            # building extra data
            #
            # building
            #     (num)  btype     ,    extra     ,   level   ,   enables
            # 37,38,39res/com/ind  , cluster data ,   level   ,      -
            #       1cur(city)     ,  build_time  ,passengers ,      -
            #       2cur(land)     ,      -       ,passengers ,      -
            #       3mon           ,      -       ,passengers ,      -
            #       5tow           ,  build-time  ,passengers ,      -
            #       7hq            ,  hq-level    ,passengers ,      -
            #  11dock"habour"      , water-waytype,   level   ,|=1:pax/|=2:post/|=4:ware
            # 36flat-dock"dock"    , water-waytype,   level   ,|=1:pax/|=2:post/|=4:ware
            #     4factory         ,      -       ,   level   ,     |=4
            # 34,35stop/extension  ,    waytype   ,   level   ,|=1:pax/|=2:post/|=4:ware
            #      33depot         ,    waytype   ,     -     ,      -
            #
            #
            # Arranging addons
            #
            # name
            name = ask_function("Name = "+str(name),name,where_show,0)
            # building type
            # no change but version difference:
            if version < 9 and write_version >= 9:
                if(old_btype_int<3):
                    btype_int = btype_tuple.index("city_res") + old_btype_int
            print_function("building type is "+btype_tuple[btype_int],where_show)
            # level
            waytype_tpl = {
                0: "None",
                1: "road_wt",
                2: "track_wt",
                3: "water_wt",
                5: "monorail_wt",
                6: "maglev_wt",
                7: "tram_wt",
                8: "narrowgauge_wt",
                16: "air_wt"
            }
            level_meaning = "level"
            Extra_meaning = ""
            if( btype_int==btype_tuple.index("attraction_city") or btype_int==btype_tuple.index("attraction_land") or btype_int==btype_tuple.index("monument") or btype_int==btype_tuple.index("townhall") or btype_int==btype_tuple.index("headquarters") ):
                level_meaning = "passangers level"
            if( btype_int==btype_tuple.index("attraction_city") or btype_int==btype_tuple.index("townhall") ):
                Extra_meaning = "build-time (the city population which this building will be constructed)"
            if( btype_int==btype_tuple.index("headquarters") ):
                Extra_meaning = "headquarter level"
            if( btype_int==btype_tuple.index("generic_stop") or btype_int==btype_tuple.index("generic_extension") or btype_int==btype_tuple.index("depot") ):
                Extra_meaning = "Waytype"
            # if( btype_int==btype_tuple.index("ciry_res") or btype_int==btype_tuple.index("city_com") or btype_int==btype_tuple.index("city_ind") ):
            #    Extra_meaning = "Cluster_data"
            level_int = ask_function(level_meaning,level_int,where_show=where_show,output_type=1)
            #extra data
            if( len(Extra_meaning)>0 ):
                if( Extra_meaning!="Waytype" ):
                    extra_data = ask_function(Extra_meaning,extra_data,where_show=where_show,output_type=1)
                else:
                    print_function(extra_data+":"+waytype_tpl[extra_data],where_show=where_show)
                    for i in range(17):
                        if(waytype_tpl.get(i)):
                            print_function(str(i)+" : "+waytype_tpl[i])
                    new_waytype = input_function(where_show=where_show)
                    if( waytype_tpl.get(new_waytype) ):
                        print_function("new waytype is "+waytype_tpl[i])
                        extra_data = new_waytype
                    else:
                        print_function("invalid input: waytype is not changed: "+waytype_tpl[extra_data])
            #climate
            if( write_version>3 ):
                allowed_climates_int = climate_changing(allowed_climates_int,where_show)
            #enable(for station)
            if( write_version>2 ):
                if( btype_tuple.index("bahnhof")<=btype_int<=btype_tuple.index("flat_dock") and btype_int!=btype_tuple.index("depot") ):
                    enables_int = change_enable_goodstype(enables_int,where_show)
            #flag
            no_info_int = build_chance_int&1
            #no_info_int = ask_function("no info? 1->true, 0->false",build_flag_int&1,where_show,1)
            #if( no_info_int != 0 and no_info_int != 1 ):
            #    print_function("invalid input, no info flag is set as "+str(build_flag_int&1),where_show)
            no_construction_int = ask_function("no construction? 1->true, 0->false",(build_flag_int&2)>>1,where_show,1)
            if( no_construction_int != 0 and no_construction_int != 1 ):
                print_function("invalid input, no construction flag is set as "+str((build_flag_int&2)>>1),where_show)
            needs_ground_int = ask_function("neeeds ground? 1->true, 0->false",(build_flag_int&4)>>2,where_show,1)
            if( needs_ground_int != 0 and needs_ground_int != 1 ):
                print_function("invalid input, needs ground flag is set as "+str((build_flag_int&4)>>2),where_show)
            build_flag_int = no_info_int + (no_construction_int<<1) + (needs_ground_int<<2)
            #chance
            # build_chance_int=ask_function("build change ")
            # intro and retire year
            if ( write_version>1 ):
                intro_y = ask_function("intro_year :"+str(intro_y),intro_y,where_show,1)
                intro_m = ask_function("intro_month:"+str(intro_m),intro_m,where_show,1)
                retire_y = ask_function("retire_year :"+str(retire_y),retire_y,where_show,1)
                retire_m = ask_function("retire_month:"+str(retire_m),retire_m,where_show,1)
            # capacity
            if( write_version>7 and btype_tuple.index("bahnhof")<=btype_int<=btype_tuple.index("flat_dock") and btype_int!=btype_tuple.index("depot") ):    
                capacity_int=ask_function("capacity:",capacity_int,where_show,1)
            # maintainance and price
            if( write_version>7 ):
                price_int=ask_function("price:",capacity_int,where_show,1)
                maintenance_int=ask_function("maintenance cost:",capacity_int,where_show,1)
            # preservation year
            if ( write_version>9 ):
                preservation_y = ask_function("preservation_year :"+str(preservation_y),preservation_y,where_show,1)
                preservation_m = ask_function("preservation_month:"+str(preservation_m),preservation_m,where_show,1)


            #
            #
            #
            # Write output nodes
            temp_headnode+=old_btype_int.to_bytes(1,byteorder="little")
            new_obj_size+=1
            temp_headnode+=btype_int.to_bytes(1,byteorder="little")
            new_obj_size+=1
            temp_headnode+=level_int.to_bytes(2,byteorder="little")
            new_obj_size+=2
            temp_headnode+=extra_data.to_bytes(4,byteorder="little")
            new_obj_size+=4
            temp_headnode+=size_x_int.to_bytes(2,byteorder="little")
            temp_headnode+=size_y_int.to_bytes(2,byteorder="little")
            temp_headnode+=layout_int.to_bytes(1,byteorder="little")
            new_obj_size+=5
            if write_version>3:
                temp_headnode+=allowed_climates_int.to_bytes(2,byteorder="little")
                new_obj_size+=2
            if write_version>2:
                temp_headnode+=enables_int.to_bytes(1,byteorder="little")
                new_obj_size+=1
            temp_headnode+=build_flag_int.to_bytes(1,byteorder="little")
            new_obj_size+=1
            temp_headnode+=build_chance_int.to_bytes(1,byteorder="little")
            new_obj_size+=1
            if write_version>1:
                temp_headnode+=(date_to_byte(intro_y,intro_m))
                temp_headnode+=(date_to_byte(retire_y,retire_m))
                new_obj_size+=4
            if write_version>4:
                temp_headnode+=animation_time.to_bytes(2,byteorder="little")
                new_obj_size+=2
            if write_version>7:
                temp_headnode+=capacity_int.to_bytes(2,byteorder="little")
                new_obj_size+=2
                if write_version<11:
                    temp_headnode+=maintenance_int.to_bytes(4,byteorder="little")
                    new_obj_size+=4
                    temp_headnode+=price_int.to_bytes(4,byteorder="little")
                    new_obj_size+=4
                else:
                    temp_headnode+=maintenance_int.to_bytes(8,byteorder="little")
                    new_obj_size+=8
                    temp_headnode+=price_int.to_bytes(8,byteorder="little")
                    new_obj_size+=8
            if write_version>6:
                temp_headnode+=allow_underground_int.to_bytes(1,byteorder="little")
                new_obj_size+=1
            if write_version>9:
                temp_headnode+=(date_to_byte(preservation_y,preservation_m))
                new_obj_size+=2
            new_node=obj_nchild
            # new node writing
            return_txt=b""
            return_txt+=new_node.to_bytes(2,byteorder="little")
            return_txt+=new_obj_size.to_bytes(2,byteorder="little")
            return_txt+=temp_headnode
            if(holdflags!=1):
                outfile.write(return_txt)
            return_txt+=write_text(outfile,name,holdflags)
            return_txt+=copy_object(infile,outfile,obj_nchild-1,holdflag=holdflags)
            if(holdflags!=1):
                return True
            else:
                return return_txt
    def read_factory_supplier(infile):
        # this is only for return information
        obj_byte = infile.read(4)
        nchild_byte = infile.read(2)
        nchild = int.from_bytes(nchild_byte,byteorder="little")
        size_node = infile.read(2)
        size = int.from_bytes(size_node,byteorder="little")
        version_byte = infile.read(2)
        size -= 2
        version = int.from_bytes(version_byte,byteorder="little")
        # since this object do not have version: it means capacity
        capacity = version
        supplier_count_byte = infile.read(2)
        size-=2
        supplier_count = int.from_bytes(supplier_count_byte,byteorder="little")
        consumption_byte = infile.read(2)
        size-=2
        consumption = int.from_bytes(consumption_byte,byteorder="little")
        dummy_byte = infile.read(2) #0x00
        size-=2
        if size==0 and nchild==1:
            #read head node completely
            name = read_xref(infile,type = b"GOOD") 
        # return value
        return [name,capacity,supplier_count,consumption] 
    def write_factory_supplier(outfile,sup_info,holdflag=0):
        write_text=b""
        write_text+=b"FSUP"
        nchild=1
        size=8
        write_text+=nchild.to_bytes(2,byteorder="little")
        write_text+=size.to_bytes(2,byteorder="little")
        name = str(sup_info[0])
        capacity = int(sup_info[1]) # capacity of the amount of this good storing
        supplier_count = int(sup_info[2]) # the number of industry which are made by construction of this factory
        consumption = int(sup_info[3]) # the rate of the goods we need to make 100% production 
        version = capacity
        write_text+=version.to_bytes(2,byteorder="little")
        write_text+=supplier_count.to_bytes(2,byteorder="little")
        write_text+=consumption.to_bytes(2,byteorder="little")
        write_text+=b"\x00"
        write_text+=b"\x00"
        write_text+=write_xref(outfile,name,type=b"GOOD",holdflag=1,fatal_flag=1) # goods need fatal_flag
        if holdflag==0:
            outfile.write(write_text)
        else:
            return write_text
    def read_factory_production(infile):
        # this is only for return information
        obj_byte = infile.read(4)
        nchild_byte = infile.read(2)
        nchild = int.from_bytes(nchild_byte,byteorder="little")
        size_node = infile.read(2)
        size = int.from_bytes(size_node,byteorder="little")
        version_byte = infile.read(2)
        size -= 2
        version = int.from_bytes(version_byte,byteorder="little")
        if(version&0x8000>0 and version&0x7FFF==1):
            capacity_byte = infile.read(2)
            size -= 2
            capacity = int.from_bytes(capacity_byte,byteorder="little")
            factor_count_byte = infile.read(2)
            size-=2
            factor = int.from_bytes(factor_count_byte,byteorder="little")
        else:
            capacity = version
            factor = 256
        if size==0 and nchild==1:
            #read head node completely
            name = read_xref(infile,type = b"GOOD") 
        # return value
        return [name,capacity,factor] 
    def write_factory_production(outfile,pro_info,holdflag=0):
        write_text=b""
        write_text+=b"FPRO"
        nchild=1
        size=6
        write_text+=nchild.to_bytes(2,byteorder="little")
        write_text+=size.to_bytes(2,byteorder="little")
        name = str(pro_info[0])
        capacity = int(pro_info[1])
        factor = int(pro_info[2])
        version = 0x8001
        write_text+=version.to_bytes(2,byteorder="little")
        write_text+=capacity.to_bytes(2,byteorder="little")
        write_text+=factor.to_bytes(2,byteorder="little")
        write_text+=write_xref(outfile,name,type=b"GOOD",holdflag=1,fatal_flag=1) # goods need fatal_flag
        if holdflag==0:
            outfile.write(write_text)
        else:
            return write_text
    def factor_to_ratio(invalue=256):
        # invalue is integer 256 = 100%
        return invalue*100//256
    def ratio_to_factor(ratio=100):
        # incalue is ratio[%]
        return ratio*256//100
    def change_goods_supplier(supplier_list,where_show):
        print_function("Supplier list",where_show)
        print_function("number\tname\tcapacity\tconnecting industry number\tconsumption rate",where_show)
        for i in range(len(supplier_list)):
            print_function(str(i)+"\t"+str(supplier_list[i][0])+"\t"+str(supplier_list[i][1])+"\t"+str(supplier_list[i][2])+"\t"+str(factor_to_ratio(supplier_list[i][3])))
        print_function("How to change? Please choose and input number",where_show)
        print_function("  1.Remove selected goods",where_show)
        print_function("  2.Add goods",where_show)
        print_function("  3.Edit capacity value",where_show)
        print_function("  4.Edit the number of connecting industry",where_show)
        print_function("  5.Edit consumption rate",where_show)
        print_function("  x.Exit",where_show)
        choice=input_function(where_show=where_show)
        if choice == "x":
            print_function("Supplier list changing done!",where_show)
            return supplier_list
        elif choice=="1" or choice=="3" or choice =="4" or choice == "5":
            if choice == "1":
                print_function("Which one do you want to remove? input the number:",where_show)
            else:
                print_function("Which one do you want to edit? input the number:",where_show)
            edit_number_str = input_function(where_show=where_show)
            try:
                edit_number=int(edit_number_str)
                if(0<=edit_number<len(supplier_list)):
                    if(choice == "1"):
                        del supplier_list[edit_number]
                        return change_goods_supplier(supplier_list,where_show)
                    else:
                        print_function("please input new value:",where_show)
                        new_value = int(input_function(where_show=where_show))
                        edit_pointer = int(choice)-2
                        if(edit_pointer == 3):
                            new_value = ratio_to_factor(new_value)
                        if new_value<0 or new_value > 0xFFFF:
                            print_function("wrong input",where_show)
                        else:
                            supplier_list[edit_number][edit_pointer] = new_value
                        return change_goods_supplier(supplier_list,where_show)

                else:
                    print_function("wrong input",where_show)
                    return change_goods_supplier(supplier_list,where_show)
            except:
                print_function("wrong input",where_show)
                return change_goods_supplier(supplier_list,where_show)
        elif choice == "2":
            print_function("which goods?",where_show)
            temp_name=input_function(where_show=where_show)
            temp_capacity=ask_function("Capacity:",1000,where_show=where_show,output_type=1)
            temp_supplier_count=ask_function("the number of supplier:",1,where_show=where_show,output_type=1)
            temp_factor=ask_function("the ratio of consumption [%]:",100,where_show=where_show,output_type=1)
            temp_sup=[temp_name,temp_capacity,temp_supplier_count,ratio_to_factor(temp_factor)]
            for i in range(len(temp_sup)-1):
                # check values
                if(temp_sup[i+1]<0 or temp_sup[i+1]>0xFFFF):
                    print_function("wrong input",where_show)
                    return change_goods_supplier(supplier_list,where_show)
            supplier_list.append(temp_sup)
            return change_goods_supplier(supplier_list,where_show)       
        else:
            print_function("wrong input",where_show)
            return change_goods_supplier(supplier_list,where_show)
    def change_goods_production(production_list,where_show):
        print_function("production list",where_show)
        print_function("number\tname\tcapacity\tproduction rate",where_show)
        for i in range(len(production_list)):
            print_function(str(i)+"\t"+str(production_list[i][0])+"\t"+str(production_list[i][1])+"\t"+str(factor_to_ratio(production_list[i][2])))
        print_function("How to change? Please choose and input number",where_show)
        print_function("  1.Remove selected goods",where_show)
        print_function("  2.Add goods",where_show)
        print_function("  3.Edit capacity value",where_show)
        print_function("  4.Edit consumption rate",where_show)
        print_function("  x.Exit",where_show)
        choice=input_function(where_show=where_show)
        if choice == "x":
            print_function("production list changing done!",where_show)
            return production_list
        elif choice=="1" or choice=="3" or choice =="4":
            if choice == "1":
                print_function("Which one do you want to remove? input the number:",where_show)
            else:
                print_function("Which one do you want to edit? input the number:",where_show)
            edit_number_str = input_function(where_show=where_show)
            try:
                edit_number=int(edit_number_str)
                if(0<=edit_number<len(production_list)):
                    if(choice == "1"):
                        del production_list[edit_number]
                        return change_goods_production(production_list,where_show)
                    else:
                        print_function("please input new value:",where_show)
                        new_value = int(edit_number_str)
                        edit_pointer = int(choice)-2
                        if(edit_pointer == 2):
                            new_value = ratio_to_factor(new_value)
                        if new_value<0 or new_value > 0xFFFF:
                            print_function("wrong input",where_show)
                            return change_goods_production(production_list,where_show)
                        else:
                            production_list[edit_number][edit_pointer] = new_value

                else:
                    print_function("wrong input",where_show)
                    return change_goods_production(production_list,where_show)
            except:
                print_function("wrong input",where_show)
                return change_goods_production(production_list,where_show)
        elif choice == "2":
            print_function("Whats the name of the good",where_show)
            temp_name=input_function(where_show=where_show)
            temp_capacity=ask_function("Capacity:",1000,where_show=where_show,output_type=1)
            temp_factor=ask_function("the ratio of production [%]:",100,where_show=where_show,output_type=1)
            temp_sup=[temp_name,temp_capacity,ratio_to_factor(temp_factor)]
            for i in range(len(temp_sup)-1):
                # check values
                if(temp_sup[i+1]<0 or temp_sup[i+1]>0xFFFF):
                    print_function("wrong input",where_show)
                    return change_goods_production(production_list,where_show)
            production_list.append(temp_sup)
            return change_goods_production(production_list,where_show)       
        else:
            print_function("wrong input",where_show)
            return change_goods_production(production_list,where_show)
    def change_placement_factory(input_int,where_show):
        return_int=input_int
        placement_list=["Land","Water","City","river","shore","forest"]
        print_function("Enable placement:"+placement_list[return_int],where_show)
        print_function("-------------------",where_show)
        print_function("Do you want to change placement? Please select changing way.",where_show)
        for i in range(len(placement_list)):
            print_function("  "+str(i)+":"+placement_list[i],where_show)
        print_function("  x:Exit (Not Change)",where_show)
        choice=input_function(where_show=where_show)
        try:
            choice_value=int(choice)
            if(0<=choice_value<len(placement_list)):
                return_int = choice_value
                print_function("new placement is "+placement_list[return_int],where_show)
        except:
            print_function("Not change placement:"+placement_list[return_int],where_show)
        return return_int
    def factory_arranging(infile,outfile,obj_nchild,obj_size):
        temp_headnode=b""
        temp_obj_size=obj_size
        new_obj_size=0
        # copy and arrange setting of vehicle
        # version
        version_byte=copy_node(infile,2)
        version_int=int.from_bytes(version_byte,byteorder="little")
        if version_int & 0x8000:
            version=version_int&0x7FFF
        else:
            version=0
        # pakfile version changing
        if version>0:
            ask_version=ask_function("Do you want to change pak version to 0x8005? yes=1,no=other","1",where_show,0)
        if ask_version=="1":
            print_function("change version",where_show)
            new_version=0x8005
            write_version=new_version&0x7FFF
        else:
            print_function("NOT change version",where_show)
            new_version=version_int
            write_version=version
        temp_headnode+=new_version.to_bytes(2,byteorder="little")
        temp_obj_size-=2
        new_obj_size+=2  
        if version<0:
            return False
        else:
            #read
            #placement
            placement_byte = infile.read(2)
            placement = int.from_bytes(placement_byte,byteorder="little")
            temp_obj_size-=2
            #productivity
            productivity_byte = infile.read(2)
            productivity = int.from_bytes(productivity_byte,byteorder="little")
            temp_obj_size-=2
            #range
            range_byte = infile.read(2)
            range_int =int.from_bytes(range_byte,byteorder="little")
            temp_obj_size-=2
            #distribution weight
            distribution_byte = infile.read(2)
            distribution_int = int.from_bytes(distribution_byte,byteorder="little")
            temp_obj_size-=2
            #color
            color_byte = infile.read(1)
            color_int = int.from_bytes(color_byte,byteorder="little")
            temp_obj_size-=1
            #fields(v>1)
            fields_int=0
            if(version>1):
                fields_byte=infile.read(1)
                fields_int=int.from_bytes(fields_byte,byteorder="little")
                temp_obj_size-=1
            #supplier count
            supplier_count_byte=infile.read(2)
            supplier_count = int.from_bytes(supplier_count_byte,byteorder="little")
            temp_obj_size-=2
            #product count
            product_count_byte = infile.read(2)
            product_count = int.from_bytes(product_count_byte,byteorder="little")
            temp_obj_size-=2
            #pax level
            pax_level_byte=infile.read(2)
            pax_level = int.from_bytes(pax_level_byte,byteorder="little")
            temp_obj_size-=2
            #expand_probability(v>2)
            expand_probability = 0
            if(version>2):
                expand_probability_byte = infile.read(2)
                expand_probability = int.from_bytes(expand_probability_byte,byteorder="little")
                temp_obj_size-=2
            #expand_minimum(v>2)
            expand_minimum = 0
            if(version>2):
                expand_minimum_byte = infile.read(2)
                expand_minimum = int.from_bytes(expand_minimum_byte,byteorder="little")
                temp_obj_size-=2
            #expand range(v>2)
            expand_range = 0
            if(version>2):
                expand_range_byte = infile.read(2)
                expand_range = int.from_bytes(expand_range_byte,byteorder="little")
                temp_obj_size-=2
            #expand_times(v>2)
            expand_times = 0
            if(version>2):
                expand_times_byte = infile.read(2)
                expand_times = int.from_bytes(expand_times_byte,byteorder="little")
                temp_obj_size-=2
            #electric_boost(v>2)
            electric_boost = 256
            if(version>2):
                electric_boost_byte = infile.read(2)
                electric_boost = int.from_bytes(electric_boost_byte,byteorder="little")
                temp_obj_size-=2
            #pax boost(v>2)
            pax_boost = 0
            if(version>2):
                pax_boost_byte = infile.read(2)
                pax_boost = int.from_bytes(pax_boost_byte,byteorder="little")
                temp_obj_size-=2
            #mail boost(v>2)
            mail_boost =0
            if(version>2):
                mail_boost_byte = infile.read(2)
                mail_boost = int.from_bytes(mail_boost_byte,byteorder="little")
                temp_obj_size-=2
            #electric demand
            electric_demand=65535
            if(version>2):
                electric_demand_byte = infile.read(2)
                electric_demand = int.from_bytes(electric_demand_byte,byteorder="little")
                temp_obj_size-=2
            #pax demand
            pax_demand = 65535
            if(version>2):
                pax_demand_byte = infile.read(2)
                pax_demand = int.from_bytes(pax_demand_byte,byteorder="little")
                temp_obj_size-=2
            #mail demand
            mail_demand=65535
            if(version>2):
                mail_demand_byte = infile.read(2)
                mail_demand = int.from_bytes(mail_demand_byte,byteorder="little")
                temp_obj_size-=2
            #sound(v>3)
            sound_interval = 0
            sound_id = 0xffff # no sound id,
            if(version>3):
                sound_interval_byte = infile.read(4)
                sound_id_byte = infile.read(1)
                temp_obj_size-=5
                sound_interval = int.from_bytes(sound_interval_byte,byteorder="little")
                sound_id = int.from_bytes(sound_id_byte,byteorder="little")
            #smoke(v>4)
            smokerotateion = 0
            b00_2 = bytes(2)
            smoketile_byte_list=[[b00_2,b00_2,b00_2,b00_2],[b00_2,b00_2,b00_2,b00_2],[b00_2,b00_2,b00_2,b00_2],[b00_2,b00_2,b00_2,b00_2]]
            smokeuplift = 0
            smokelifetime = 0
            if(version>4):
                smokerotateion_byte = infile.read(1)
                temp_obj_size-=1
                smokerotateion=int.from_bytes(smokerotateion_byte,byteorder="little")
                for i in range(4):
                    for j in range(4):
                        smoketile_byte_list[i][j]=infile.read(2)
                        temp_obj_size-=2
                smokeuplift_byte=infile.read(2)
                temp_obj_size-=2
                smokeuplift = int.from_bytes(smokeuplift_byte,byteorder="little")
                smokelifetime_byte=infile.read(2)
                temp_obj_size-=2
                smokelifetime = int.from_bytes(smokelifetime_byte,byteorder="little")
            # sound
            sound_details_byte = b""
            if( sound_id == 0xfffe or temp_obj_size >0 ):
                sound_details_byte = infile.read(temp_obj_size)
                temp_obj_size = 0


            # the next node is building
            building_node = copy_object(infile,outfile,1,holdflag=1,bytes=b"",need_return=1)

            # other node (smoke)
            smoke_node = copy_object(infile,outfile,1,holdflag=1,bytes=b"",need_return=1)

            # supplier node
            supplier_list=[]
            for i in range(supplier_count):
                supplier_list.append(read_factory_supplier(infile))
            # production node
            production_list=[]
            for i in range(product_count):
                production_list.append(read_factory_production(infile))

            # field node
            field_node = b""
            if(obj_nchild-2-supplier_count-product_count > 0):
                field_node+=copy_object(infile,outfile,obj_nchild-2-supplier_count-product_count,holdflag=1,bytes=b"",need_return=1)

            # arrange
            # some value's change are already done in building_arrange()
            # placement
            placement = change_placement_factory(placement,where_show)
            # productivity
            productivity = ask_function("productivity",answer=productivity,where_show=where_show,output_type=1)
            # range
            range_int = ask_function("productivity range",range_int,where_show,1)
            # distribution weight
            distribution_int=ask_function("distribution weight",distribution_int,where_show,1)
            # color
            # nochange
            # field 
            # nochange
            # supplier
            obj_nchild-=supplier_count
            supplier_list=change_goods_supplier(supplier_list,where_show)
            supplier_count = len(supplier_list)
            obj_nchild+=supplier_count
            # production         
            obj_nchild-=product_count   
            production_list=change_goods_production(production_list,where_show)
            product_count = len(production_list)
            obj_nchild+=product_count
            # pax level
            pax_level = ask_function("pax lavel",answer=pax_level,where_show=where_show,output_type=1)
            if(write_version>2):
                # expand probability
                expand_probability = ask_function("expand probability",expand_probability,where_show,1)
                # expand range
                expand_range = ask_function("expand range",expand_range,where_show,1)
                # expand times
                expand_times = ask_function("expand times",expand_times,where_show,1)
                # electric boost
                electric_boost = ask_function("electric boost",electric_boost,where_show,1)
                # pax boost
                pax_boost = ask_function("pax boost",pax_boost,where_show,1)
                # mail boost
                mail_boost= ask_function("mail boost",mail_boost,where_show,1)
                # electric demand
                electric_demand = ask_function("electric demand",electric_demand,where_show,1)
                # pax demand
                pax_demand = ask_function("pax demand",pax_demand,where_show,1)
                # mail demand
                mail_demand = ask_function("mail demand",mail_demand,where_show,1)
            

            # output
            #placement
            temp_headnode+= placement.to_bytes(2,byteorder="little")
            new_obj_size+=2
            #productivity
            temp_headnode+=productivity.to_bytes(2,byteorder="little")
            new_obj_size+=2
            #range
            temp_headnode+=range_int.to_bytes(2,byteorder="little")
            new_obj_size+=2
            #distribution weight
            temp_headnode+=distribution_int.to_bytes(2,byteorder="little")
            new_obj_size+=2
            #color
            temp_headnode+=color_int.to_bytes(1,byteorder="little")
            new_obj_size+=1
            #fields(v>1)
            if(new_version>1):
                temp_headnode+=fields_int.to_bytes(1,byteorder="little")
                new_obj_size+=1
            #supplier count
            temp_headnode+=supplier_count.to_bytes(2,byteorder="little")
            new_obj_size+=2
            #product count
            temp_headnode+=product_count.to_bytes(2,byteorder="little")
            new_obj_size+=2
            #pax level
            temp_headnode+=pax_level.to_bytes(2,byteorder="little")
            new_obj_size+=2
            #expand_probability(v>2)
            if(new_version>2):
                temp_headnode+=expand_probability.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #expand_minimum(v>2)
            if(new_version>2):
                temp_headnode+=expand_minimum.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #expand range(v>2)
            if(new_version>2):
                temp_headnode+=expand_range.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #expand_times(v>2)
            if(new_version>2):
                temp_headnode+=expand_times.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #electric_boost(v>2)
            if(new_version>2):
                temp_headnode+=electric_boost.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #pax boost(v>2)
            if(new_version>2):
                temp_headnode+=pax_boost.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #mail boost(v>2)
            if(new_version>2):
                temp_headnode+=mail_boost.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #electric demand
            if(new_version>2):
                temp_headnode+=electric_demand.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #pax demand
            if(new_version>2):
                temp_headnode+=pax_demand.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #mail demand
            if(new_version>2):
                temp_headnode+=mail_demand.to_bytes(2,byteorder="little")
                new_obj_size+=2
            #sound(v>3)
            if(new_version>3):
                temp_headnode+=sound_interval.to_bytes(4,byteorder="little")
                temp_headnode+=sound_id.to_bytes(1,byteorder="little")
                new_obj_size+=5
            #smoke(v>4)
            if(new_version>4):
                temp_headnode+=smokerotateion.to_bytes(1,byteorder="little")
                new_obj_size+=1
                for i in range(4):
                    for j in range(4):
                        temp_headnode+=smoketile_byte_list[i][j]
                        new_obj_size+=2
                new_obj_size+=2
                temp_headnode+=smokeuplift.to_bytes(2,byteorder="little")
                new_obj_size+=2
                temp_headnode+=smokelifetime.to_bytes(2,byteorder="little")
            # sound file name
            temp_headnode+=sound_details_byte
            new_obj_size+=len(sound_details_byte)
            new_node=obj_nchild
            # new node writing
            return_txt=b""
            return_txt+=new_node.to_bytes(2,byteorder="little")
            return_txt+=new_obj_size.to_bytes(2,byteorder="little")
            return_txt+=temp_headnode
            outfile.write(return_txt)


            # the next node is building
            outfile.write(building_node)

            # other node (smoke)
            outfile.write(smoke_node)

            # supplier node
            for i in range(supplier_count):
                write_factory_supplier(outfile,supplier_list[i])
            # production node
            for i in range(product_count):
                write_factory_production(outfile,production_list[i])

            # field node
            outfile.write(field_node)
            return True


            




    samefile_flag=0
    if infile_path==outfile_path:
        samefile_flag=1
        print_function("an output file and an input file are same.")
        outfile_path="temp_"+outfile_path

    try:
        infile=open(infile_path,"br")
        outfile=open(outfile_path,"bw")
    except Exception:
        print_function("No file!",where_show)
        return False
    a=copy_header(infile,outfile)
    if not a:
        return False
    a=copy_root(infile,outfile)
    if not a:
        return False
    infile.close()
    outfile.close()
    if samefile_flag==1:
        os.rename(infile_path,infile_path[:-4]+"_old.pak")
        os.rename(outfile_path,infile_path)
    if a:
        print_function("pak arranging is done!",where_show)



if __name__ == "__main__":
    main()