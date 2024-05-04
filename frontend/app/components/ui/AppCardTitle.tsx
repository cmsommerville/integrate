export default function AppCardTitle({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="mb-6">
      <h2 className="text-lg">{children}</h2>
      <hr className="my-2" />
    </div>
  );
}
