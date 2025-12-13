import { WordList } from "@/components/WordList";

export default function Page() {
  return (
    <div className="flex-1 w-full overflow-auto flex justify-center items-start py-4">
      <WordList />
    </div>
  );
}
