/* The roster. One object per person; delete the placeholders, add the team.
   The real list lives in Hub Roster (P IDs). Copy public columns only: never
   email, school contact or parent details.

     pid    P ID from Hub Roster. Not shown on the page except as a fallback tile
     name   the name to publish
     role   "Team Lead", "Advisor", "Instructor", "PI" ... ; leave "" for students
     track  sub-team, used as the filter ("Wet Lab", "Dry Lab", "Human Practices")
     photo  https://static.igem.wiki/teams/TEAM_ID/wiki/team/P001_Portrait_v1.jpg, or "" for a tile
            A portrait needs a K row in Hub Consent that allows publishing it
     bio    two or three sentences the person wrote themselves
     tasks  short task names, shown as pills                                   */
window.ROSTER = [
  { pid: "P___", name: "[Member name]", role: "", track: "Wet Lab", photo: "", bio: "[Bio written by the person, 2 to 3 sentences]", tasks: ["[Task]"] },
  { pid: "P___", name: "[Member name]", role: "", track: "Dry Lab", photo: "", bio: "[Bio written by the person, 2 to 3 sentences]", tasks: ["[Task]"] },
  { pid: "P___", name: "[Member name]", role: "", track: "Human Practices", photo: "", bio: "[Bio written by the person, 2 to 3 sentences]", tasks: ["[Task]"] },
  { pid: "P___", name: "[Advisor name]", role: "Advisor", track: "Advisors", photo: "", bio: "[Bio written by the person, 2 to 3 sentences]", tasks: ["[Task]"] },
  { pid: "P___", name: "[Instructor name]", role: "Instructor", track: "Instructors and PI", photo: "", bio: "[Bio written by the person, 2 to 3 sentences]", tasks: ["[Task]"] }
];
