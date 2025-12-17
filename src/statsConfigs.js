export const positionStats = {
  CB: ["Gls", "Tkl", "Int", "Clr", "Blocks", "Cmp", "xA", "TklW"],
  FB: ["Gls", "Tkl", "Int", "Cmp", "PrgC", "PrgP", "Ast", "Clr"],
  WB: ["Gls", "Tkl", "Int", "PrgC", "PrgP", "Ast", "Clr"],
  DM: ["Gls", "Tkl", "Int", "PrgP", "Cmp", "Blocks", "xA", "Ast", "KP"],
  CM: ["Gls", "Cmp", "PrgP", "Ast", "KP", "Tkl", "Int", "xA"],
  AM: ["Gls", "Ast", "KP", "xA", "PrgP", "xG", "Cmp", "PrgC"],
  ST: ["Gls", "xG", "Sh", "SoT", "Ast", "xA"],
  W: ["Gls", "Ast", "xA", "PrgC", "xG", "onethird", "CPA", "Att", "Succ"],
};

export const positionMapping = {
  DF: ["CB", "FB", "WB"],
  MF: ["DM", "CM", "AM"],
  FW: ["ST", "W"],
};

export const defaultPositionStats = {
  DF: ["Tkl", "Int", "Clr", "Blocks", "Cmp"],
  MF: ["Cmp", "PrgP", "Ast", "KP", "Tkl", "Int"],
  FW: ["Gls", "xG", "Sh", "SoT", "Ast", "xA"],
};

export const statNames = {
  Tkl: "Tackles",
  Tklw: "Tackles that won team possesions",
  Int: "Interceptions",
  Clr: "Clearances",
  Blocks: "Blocks",
  Cmp: "Cmpes",
  xA: "Expected Assists",
  PrgC: "Progressive Carries",
  PrgP: "Progressive Passes",
  Ast: "Assists",
  KP: "Key Passes",
  Gls: "Goals",
  xG: "Expected Goals",
  Sh: "Shots",
  SoT: "Shots on Target",
  onethird: "Carries into the Final Third",
  CPA: "Carries into Penalty Area",
  Att: "Dribbles Attempted",
  Succ: "Successful Dribbles",
  Cmp: "Completed passes",
};
