export interface ProcessStep {
  name: string;
  href: string;
  status: "COMPLETE" | "CURRENT" | "INCOMPLETE";
}
