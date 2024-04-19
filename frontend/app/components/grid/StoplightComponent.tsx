"use client";

export default function StoplightComponent(params: any) {
  const { colorFormatter } = params;

  if (!colorFormatter) {
    return (
      <span className="bg-green-500/20 py-1 px-4 rounded-full">
        {params.valueFormatted}
      </span>
    );
  }
  if (colorFormatter(params) === "red") {
    return (
      <span className="bg-red-500/20 py-1 px-4 rounded-full">
        {params.valueFormatted}
      </span>
    );
  }

  if (colorFormatter(params) === "yellow") {
    return (
      <span className="bg-yellow-500/20 py-1 px-4 rounded-full">
        {params.valueFormatted}
      </span>
    );
  }
  return (
    <span className="bg-green-500/20 py-1 px-4 rounded-full">
      {params.valueFormatted}
    </span>
  );
}
