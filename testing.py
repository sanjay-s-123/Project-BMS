blood_avai = ["a+ve", "b+ve", "o+ve", "a-ve", "b-ve", "o-ve", "ab+ve", "ab-ve"]
availability_status = False
def hosp():
    hosp_name = input("Enter the Hospital Name:")
    blood_type = input("Blood type: ")
    for is_avai in blood_avai:
        if is_avai == blood_type:
            availability_status = True
            print(availability_status)
            break
    else:
        print("Type not found.")

hosp()