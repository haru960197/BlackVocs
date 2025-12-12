"use client";

import { useEffect, useRef, useState } from "react";

// 型定義
type WordData = {
  id: string;
  term: string;
  definition: string;
  example?: string;
};

type WordDetailModalProps = {
  isOpen: boolean;
  onClose: () => void;
  wordId: string | null; // IDのみを受け取る
};

// 【ダミーAPI】実際の開発ではここを fetch("/api/words/...") などに置き換えます
const mockFetchWord = async (id: string): Promise<WordData> => {
  // ネットワーク遅延をシミュレート (0.5秒)
  await new Promise((resolve) => setTimeout(resolve, 500));

  return {
    id,
    term: `Word-${id}`, // 実際はDBから取得した値
    definition: `これはID: ${id} の詳細な定義です。サーバーから取得しました。`,
    example: "This is an example sentence fetched from the server.",
  };
};

export const WordDetailModal = ({ isOpen, onClose, wordId }: WordDetailModalProps) => {
  const dialogRef = useRef<HTMLDialogElement>(null);

  // 内部で保持するデータとローディング状態
  const [data, setData] = useState<WordData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // 1. モーダルの開閉制御（前回と同じロジック）
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      if (!dialog.open) dialog.showModal();
    } else {
      if (dialog.open) dialog.close();
    }
  }, [isOpen]);

  // 2. データ取得ロジック（wordIdが変わったら走る）
  useEffect(() => {
    // IDがない、またはモーダルが閉じている場合はリセットして何もしない
    if (!wordId || !isOpen) {
      setData(null);
      return;
    }

    let ignore = false; // クリーンアップ用フラグ（競合防止）

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const result = await mockFetchWord(wordId);
        if (!ignore) setData(result);
      } catch (error) {
        console.error("Failed to fetch", error);
      } finally {
        if (!ignore) setIsLoading(false);
      }
    };

    fetchData();

    return () => {
      ignore = true;
    };
  }, [wordId, isOpen]);

  const handleClose = () => {
    onClose();
  };

  return (
    <dialog ref={dialogRef} className="modal" onClose={handleClose}>
      <div className="modal-box">
        {/* ローディング中の表示 */}
        {isLoading && (
          <div className="flex justify-center items-center py-10">
            <span className="loading loading-spinner loading-lg text-primary"></span>
          </div>
        )}

        {/* データ表示（ローディングが終わってデータがある場合） */}
        {!isLoading && data && (
          <>
            <h3 className="font-bold text-2xl mb-2">{data.term}</h3>
            <div className="badge badge-outline mb-4">ID: {data.id}</div>

            <p className="text-gray-600 mb-2">意味:</p>
            <p className="text-lg mb-4">{data.definition}</p>

            {data.example && (
              <div className="alert">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  className="stroke-info shrink-0 w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
                <span>Example: {data.example}</span>
              </div>
            )}
          </>
        )}

        {/* エラーやデータなしの場合の簡易表示 */}
        {!isLoading && !data && wordId && (
          <p className="text-error">データの取得に失敗しました。</p>
        )}

        <div className="modal-action">
          <button className="btn" onClick={handleClose}>
            閉じる
          </button>
        </div>
      </div>

      <form method="dialog" className="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
  );
};
