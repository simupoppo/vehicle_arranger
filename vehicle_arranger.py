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
    print_function(texts,where_show)
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
            for j in range(input_list):
                if climate_list[i]==input_list[j]:
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
            if str(choice)==1:
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
            elif str(choice)==2:
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
        print_function("  x.Exit")
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
    def read_xref(infile):
        xref=infile.read(4)
        xref_nchild=infile.read(2)
        xref_size_byte=infile.read(2)
        xref_size=int.from_bytes(xref_size_byte,byteorder="little")
        VHCL=infile.read(4)
        cflag=infile.read(1)
        output=infile.read(xref_size-6)
        infile.read(1)
        if xref==b"XREF" and xref_nchild==b"\x00\x00" and VHCL==b"VHCL" and cflag==b"\x00":
            return output.decode("utf-8")
    def write_xref(outfile,text):
        outfile.write(b"XREF")
        outfile.write(b"\x00\x00")#must be a child
        size_int=4+1+len(text)+1
        outfile.write(size_int.to_bytes(2,byteorder="little"))
        outfile.write(b"VHCL")
        outfile.write(b"\x00")#Fatal-Flag
        outfile.write(text.encode("utf-8"))
        outfile.write(b"\x00")
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
            ask_version=ask_function("Do you want to change pak version to 0x800B? yes=1,no=other","1",where_show,0)
        if ask_version=="1":
            print_function("change version",where_show)
            new_version=0x800b
            write_version=new_version&0x7FFF
        else:
            print_function("NOT change version",where_show)
            new_version=version|0x8000
            write_version=version
        temp_headnode+=new_version.to_bytes(2,byteorder="little")
        temp_obj_size-=2
        new_obj_size+=2
        if version>0:
            # cost
            price_byte32 = infile.read(4)
            price = int.from_bytes(price_byte32,byteorder="little")
            price = ask_function("cost = "+str(price),price,where_show,1)
            temp_headnode+=(price.to_bytes(4,byteorder="little"))
            temp_obj_size-=4
            new_obj_size+=4
            # capacity
            capacity_byte = infile.read(2)
            price = int.from_bytes(capacity_byte,byteorder="little")
            price = ask_function("capacity = "+str(price),price,where_show,1)
            temp_headnode+=(price.to_bytes(2,byteorder="little"))
            temp_obj_size-=2
            new_obj_size+=2
            # loading_time
            if version>8:
                # depends on the version
                l_time_byte = infile.read(2)
                temp_obj_size-=2
                l_time = int.from_bytes(l_time_byte,byteorder="little")
            else:
                l_time = 1000
            if write_version>8:
                l_time = ask_function("loading time = "+str(l_time),l_time,where_show,1)
                temp_headnode+=(l_time.to_bytes(2,byteorder="little"))
                new_obj_size+=2
            # speed
            speed_byte = infile.read(2)
            speed_int = int.from_bytes(speed_byte,byteorder="little")
            speed_int = ask_function("top speed = "+str(speed_int),speed_int,where_show,1)
            temp_headnode+=(speed_int.to_bytes(2,byteorder="little"))
            temp_obj_size-=2
            new_obj_size+=2
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
            weight = ask_function("weight = "+str(weight),weight,where_show,1)
            if write_version>9:
                temp_headnode+=(weight.to_bytes(4,byteorder="little"))
                new_obj_size+=4
            else:
                temp_headnode+=(weight.to_bytes(2,byteorder="little"))
                new_obj_size+=2
            # axle_load
            if version>8:
                axle_byte=infile.read(2)
                axle_int=int.from_bytes(axle_byte,byteorder="little")
                temp_obj_size-=2
            else:
                axle_int=0
            if write_version>8:
                axle_int=ask_function("axle_load="+str(axle_int),axle_int,where_show,1)
                temp_headnode+=(axle_int.to_bytes(2,byteorder="little"))
                new_obj_size+=2  
            # power
            if version>5:
                power_byte32 = infile.read(4)
                temp_obj_size-=4
            else:
                power_byte32 = infile.read(2)
                temp_obj_size-=2
            power = int.from_bytes(power_byte32,byteorder="little")
            power = ask_function("power = "+str(power)+"kW",power,where_show,1)
            if write_version>5:
                temp_headnode+=(power.to_bytes(4,byteorder="little"))
                new_obj_size+=4
            else:
                temp_headnode+=(power.to_bytes(2,byteorder="little"))
                new_obj_size+=2
            # running cost
            rcost_byte = infile.read(2)
            rcost = int.from_bytes(rcost_byte,byteorder="little")
            rcost = ask_function("running cost = "+str(rcost),rcost,where_show,1)
            temp_headnode+=(rcost.to_bytes(2,byteorder="little"))
            temp_obj_size-=2
            new_obj_size+=2
            # monthly maintenance
            # depends on the version
            if version >8:
                if version>10:
                    mcost_byte32 = infile.read(4)
                    temp_obj_size-=4
                else:
                    mcost_byte32 = infile.read(2)
                    temp_obj_size-=2
                mcost = int.from_bytes(mcost_byte32,byteorder="little")
            else:
                mcost = 0
            if write_version>8:
                mcost = ask_function("mcost = "+str(mcost),mcost,where_show,1)
                if write_version>10:
                    temp_headnode+=(mcost.to_bytes(4,byteorder="little"))
                    new_obj_size+=4
                else:
                    temp_headnode+=(mcost.to_bytes(2,byteorder="little"))
                    new_obj_size+=2
        else:
            print_function("Too old",where_show)
            return False
        # Intro year
        intro_byte = infile.read(2)
        if version<5:
            intro_y,intro_m = byte_to_date(intro_byte,version=0)
        else:
            intro_y,intro_m = byte_to_date(intro_byte)
        intro_y = ask_function("intro_year :"+str(intro_y),intro_y,where_show,1)
        intro_m = ask_function("intro_month:"+str(intro_m),intro_m,where_show,1)
        temp_headnode+=(date_to_byte(intro_y,intro_m))
        temp_obj_size-=2
        new_obj_size+=2
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
        if write_version>2:
            retire_y = ask_function("retire_year :"+str(retire_y),retire_y,where_show,1)
            retire_m = ask_function("retire_month:"+str(retire_m),retire_m,where_show,1)
            if version<5:
                temp_headnode+=(date_to_byte(retire_y,retire_m,version=0))
            else:
                temp_headnode+=(date_to_byte(retire_y,retire_m))
            new_obj_size+=2
        # Engine gear
        if version>5:
            gear_byte=infile.read(2)
            temp_obj_size-=2
        else:
            gear_byte=infile.read(1)
            temp_obj_size-=1
        gear_int=int.from_bytes(gear_byte,byteorder="little")
        if write_version>5:
            temp_headnode+=(gear_int.to_bytes(2,byteorder="little"))
            new_obj_size+=2
        else:
            temp_headnode+=(gear_int.to_bytes(1,byteorder="little"))
            new_obj_size+=1
        # waytype
        temp_headnode+=copy_node(infile,1)
        temp_obj_size-=1
        new_obj_size+=1
        # sound id
        temp_headnode+=copy_node(infile,1)
        temp_obj_size-=1
        new_obj_size+=1
        # engine type
        temp_headnode+=copy_node(infile,1)
        temp_obj_size-=1
        new_obj_size+=1
        # length
        if version>6:
            vlength_byte=infile.read(1)
            vlength_int=int.from_bytes(vlength_byte,byteorder="little")
            temp_obj_size-=1
        else:
            vlength_int=8
        vlength_int = ask_function("mcost = "+str(vlength_int),vlength_int,where_show,1)
        if write_version>6:
            temp_headnode+=(vlength_int.to_bytes(1,byteorder="little"))
            new_obj_size+=1

        
        # leader reading
        leader_byte=infile.read(1)
        leader=int.from_bytes(leader_byte,byteorder="little")
        temp_obj_size-=1
        new_obj_size+=1
        # trailer reading
        trailer_byte=infile.read(1)
        trailer=int.from_bytes(trailer_byte,byteorder="little")
        temp_obj_size-=1
        new_obj_size+=1
        # freight image number (only for version updating)
        others_byte=b""
        if version<8 and write_version>7:
            freight_image_number_int=0
            others_byte+=freight_image_number_int.to_bytes(1,byteorder="little")
            new_obj_size+=1
        # other_params_reading
        others_byte+=infile.read(temp_obj_size)
        others_byte+=copy_object(infile,outfile,6,holdflag=1,bytes=b"",need_return=1)
        new_obj_size+=temp_obj_size
        temp_obj_size=0
        # leader and trailer reading
        temp_leaders=[]
        temp_trailers=[]
        for i in range(leader):
            temp_leaders.append(read_xref(infile))
        for i in range(trailer):
            temp_trailers.append(read_xref(infile))
        # leader and trailer changing
        result_leader_list=connecting_changing(temp_leaders,"leader")
        result_trailer_list=connecting_changing(temp_trailers,l_or_r= "trailer")
        new_node=obj_nchild-leader-trailer+len(result_leader_list)+len(result_trailer_list)
        # new node writing
        outfile.write(new_node.to_bytes(2,byteorder="little"))
        outfile.write(new_obj_size.to_bytes(2,byteorder="little"))
        outfile.write(temp_headnode)
        outfile.write(len(result_leader_list).to_bytes(1,byteorder="little"))
        outfile.write(len(result_trailer_list).to_bytes(1,byteorder="little"))
        outfile.write(others_byte)
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

    def building_arranging(infile,outfile,obj_nchild,obj_size):
        btype_tuple=(
            "unknown",#0
            "attraction_city",#1
            "attraction_land",#2
            "monument",#3
            "factory",#4
            "townhall",#5
            "others",#6
            "headquarters",#7
            "bahnhof",#8,old_building_types
            "bushalt",#9,old_building_types
            "ladebucht",#10,old_building_types
            "dock",#11
            "binnenhafen",#12,old_building_types
            "airport",#13,old_building_types
            "monorailstop",#14,old_building_types
            "",#15 is empty
            "bahnhof_geb",#16,old_building_types
            "bushalt_geb",#17,old_building_types
            "ladebucht_geb",#18,old_building_types
            "hagen_geb",#19,old_building_types
            "binnenhafen_geb",#20,old_building_types
            "airport_geb",#21,old_building_types
            "monorail_geb",#22,old_building_types
            "",#23 is empty
            "",#24 is empty
            "",#25 is empty
            "",#26 is empty
            "",#27 is empty
            "",#28 is empty
            "",#29 is empty
            "wartehalle",#30,old_building_types
            "mail",#31,old_building_types
            "lagerhalle",#32,old_building_types
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
            ask_version=ask_function("Do you want to change pak version to 0x800A? yes=1,no=other","1",where_show,0)
        if ask_version=="1":
            print_function("change version",where_show)
            new_version=0x800a
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
                maintenance_byte=infile.read(4)
                temp_obj_size-=4
                maintenance_int=int.from_bytes(maintenance_byte,byteorder="little")
                price_byte=infile.read(4)
                temp_obj_size-=4
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
            #
            # building extra data
            #
            # building
            #      btype     ,    extra     ,   level   ,   enables
            #   res/com/ind  , cluster data ,   level   ,      -
            #       cur      , if 1 -> city ,passengers ,      -
            #       cur      , if 0 -> land ,passengers ,      -
            #       mon      ,      -       ,passengers ,      -
            #       tow      ,  build-time  ,passengers ,      -
            #       hq       ,  hq-level    ,passengers ,      -
            #   dock"habour" , water-waytype,   level   ,      -
            # flat-dock"dock", water-waytype,   level   ,      -
            #     factory    ,      -       ,   level   ,     |=4
            # stop/extension ,    waytype   ,   level   ,|=1:pax/|=2:post/|=4:ware
            #      depot     ,    waytype   ,     -     ,      -
            #
            #
            # Arranging addons
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
                temp_headnode+=maintenance_int.to_bytes(4,byteorder="little")
                new_obj_size+=4
                temp_headnode+=price_int.to_bytes(4,byteorder="little")
                new_obj_size+=4
            if write_version>6:
                temp_headnode+=allow_underground_int.to_bytes(1,byteorder="little")
                new_obj_size+=1
            if write_version>9:
                temp_headnode+=(date_to_byte(preservation_y,preservation_m))
                new_obj_size+=2
            new_node=obj_nchild
            # new node writing
            outfile.write(new_node.to_bytes(2,byteorder="little"))
            outfile.write(new_obj_size.to_bytes(2,byteorder="little"))
            outfile.write(temp_headnode)
            copy_object(infile,outfile,obj_nchild,holdflag=0)
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