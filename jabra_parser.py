"""Parse an exported csv from the Jabra Sports Life app 
    and returns a dict and an array of dicts with the summary of the workout
    and the trackpoints of the activity respectively"""
class Parser:
    workout_summ = {}
    workout_data = []    

    def __init__(self, summary_filename, filename):
        self.summary_filename = summary_filename
        self.filename = filename
        self.read_summary()
        self.read_activity_file()

    def read_summary(self):
        with open(self.summary_filename) as f:
            summ_keys = f.readline().strip().split(";") 
            values =  f.readline().strip().replace(",",".").split(";")            
            # Merge the two lists to create a dictionary
            self.workout_summ = dict(zip(summ_keys,values))

    def read_activity_file(self):
        with open(self.filename) as f:
            point_keys = f.readline().strip().split(";") 
            for line in f:
                workout_trackpoint = dict(zip(point_keys,line.strip().replace(",",".").split(";")))
                self.workout_data.append(workout_trackpoint)
    
    def get_data(self):
        return self.workout_summ, self.workout_data


def main():
    """Usage example"""
    summary_filename = ""
    filename = ""
    p = Parser(summary_filename,filename)
    summ, data = p.get_data()
    
if __name__== "__main__":
    main()