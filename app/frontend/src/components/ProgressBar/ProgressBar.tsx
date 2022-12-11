type Props = {
  progress: number;
  colorClass?: string;
};

const ProgressBar = ({ progress, ...props }: Props) => {
  return (
    <div className="w-full bg-gray-200 rounded-full h-2.5">
      <div
        className={`${props.colorClass ?? "bg-primary-600"} h-2.5 rounded-full`}
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  );
};

export default ProgressBar;
