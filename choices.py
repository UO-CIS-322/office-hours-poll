"""
choices: Office hours poll choices, factored out so that
   they can be used by programs that query and reformat the database
"""

CHOICES = [ { "day": "Tuesday",
              "periods": [ "11:30a", "12:00p", "12:30p", "1:00p", "1:30p",
                           "2:00p", "2:30p", "3:00p", "5:00p", "5:30p" ]}, 
            { "day": "Wednesday",
              "periods": [ "10:00a", "10:30a", "11:00a", "11:30a", "12:00p",
                           "2:30p", "3:00p", "3:30p", "4:00p", "4:30p", "5:00p",
                           "5:30p" ]}, 
            { "day": "Thursday",
              "periods": [ "9:00a", "9:30a", "11:30a", "12:00p", "12:30p", "1:00p", "1:30p",
                           "2:00p", "2:30p", "3:00p", "5:00p", "5:30p" ]}, 
            ]
