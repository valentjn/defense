#!/usr/bin/python3

import argparse



def parseList(x): return [int(y.strip()) for y in x.split(",")]

def parseTime(x):
  x = x.split(":")
  return int(x[0])*60 + int(x[1])

def formatTime(x): return "{}:{:02.0f}".format(x // 60, x % 60)

def main():
  parser = argparse.ArgumentParser(
      description="Parse timing output of impressive.")
  parser.add_argument(
      "inputPath", metavar="FILE", help="Path to text output of impressive")
  args = parser.parse_args()
  
  with open(args.inputPath, "r") as f: text = f.read()
  
  lines = text.splitlines()
  frameSlides   = parseList(lines[0])
  sectionSlides = parseList(lines[1])
  del lines[:2]
  
  fields = [x.split() for x in lines
           if (len(x) > 0) and (x[-1] in "0123456789") and
           (x[:4] != "over")]
  slides = {
    int(x[0]) : {
      "duration" : int(round(parseTime(x[1]) * 1.0275)),
      "enter"    : parseTime(x[2]),
      "leave"    : parseTime(x[3]),
    }
    for x in fields
  }
  
  slideDurations = [(slides[x]["duration"] if x >= 2 else 0)
                    for x in range(frameSlides[-1] + 1)]
  frameDurations = [sum(slideDurations[frameSlides[i]:frameSlides[i+1]])
                    for i in range(1, len(frameSlides)-1)]
  sectionDurations = [sum(slideDurations[sectionSlides[i]:sectionSlides[i+1]])
                      for i in range(len(sectionSlides)-1)]
  
  formatStr = "{:>5s}  {:>8s}"
  print(formatStr.format("Frame", "Duration"))
  print(15 * "-")
  currentSection = 1
  
  for i in range(len(frameDurations)):
    print(formatStr.format(
        "{:2.0f}".format(i), formatTime(frameDurations[i])))
    if frameSlides[i+2] >= sectionSlides[currentSection]:
      print("---- Section {}: {}".format(
          currentSection, formatTime(sectionDurations[currentSection-1])))
      currentSection += 1
  
  print("Total time without movie: {}".format(
      formatTime(sum(sectionDurations))))
  print("Total time with movie: {}".format(
      formatTime(sum(sectionDurations) + 150)))



if __name__ == "__main__":
  main()
