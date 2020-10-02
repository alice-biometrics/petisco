# import os
#
# from petisco import Petisco
#
# ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
#
#
# def petisco_config():
#     petisco = Petisco.from_filename(ROOT_PATH + "/petisco.yml")
#     petisco.configure_events(ROOT_PATH + "/petisco.events.yml")
#
#
# def main():
#     petisco_config()
#     Petisco.get_instance().start()
#
#
# if __name__ == "__main__":
#     main()
