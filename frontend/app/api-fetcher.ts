const ROOT = "http://127.0.0.1:5000";

export function GET(input: string, init?: Omit<RequestInit, "method">) {
  return fetch(`${ROOT}${input}`, {
    ...(init ? init : {}),
    method: "GET",
  });
}

export function POST(input: string, init?: Omit<RequestInit, "method">) {
  return fetch(`${ROOT}${input}`, {
    ...(init ? init : {}),
    method: "POST",
  });
}

export function PATCH(input: string, init?: Omit<RequestInit, "method">) {
  return fetch(`${ROOT}${input}`, {
    ...(init ? init : {}),
    method: "PATCH",
  });
}

export function PUT(input: string, init?: Omit<RequestInit, "method">) {
  return fetch(`${ROOT}${input}`, {
    ...(init ? init : {}),
    method: "PUT",
  });
}

export function DELETE(input: string, init?: Omit<RequestInit, "method">) {
  return fetch(`${ROOT}${input}`, {
    ...(init ? init : {}),
    method: "DELETE",
  });
}
