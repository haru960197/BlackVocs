"use client";

import { useEffect, useRef, useState } from "react";
import { WordInfo } from "@/types/word";
import { BiSolidTrash } from "react-icons/bi";
import { useToast } from "@/context/ToastContext";
import { handleDeleteWord, handleGetWordInfo } from "./actions";

type WordDetailModalProps = {
  isOpen: boolean;
  onClose: () => void;
  wordId: string | null;
};

export const WordDetailModal = ({ isOpen, onClose, wordId }: WordDetailModalProps) => {
  const dialogRef = useRef<HTMLDialogElement>(null);

  const [data, setData] = useState<WordInfo | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isDeleting, setIsDeleting] = useState<boolean>(false);
  const { showToast } = useToast();

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      if (!dialog.open) dialog.showModal();
    } else {
      if (dialog.open) dialog.close();
    }
  }, [isOpen]);

  useEffect(() => {
    if (!wordId || !isOpen) {
      setData(null);
      return;
    }

    let ignore = false; // クリーンアップ用フラグ（競合防止）

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const result = await handleGetWordInfo(wordId);

        if (!ignore && result.data) {
          setData(result.data);
        }
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

  const handleDeleteClick = async () => {
    if (!wordId) return;

    setIsDeleting(true);

    const res = await handleDeleteWord(wordId);

    setIsDeleting(false);
    onClose();

    if (res.success) {
      showToast("削除に成功しました", "success");
    } else {
      showToast("削除に失敗しました", "error");
    }
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

        {/* データ表示 */}
        {!isLoading && data && (
          <>
            <fieldset className="fieldset">
              <legend className="fieldset-legend border-b-2 w-18 pl-1 text-xl">英単語</legend>
              <p className="text-3xl p-2">{data.spelling}</p>
            </fieldset>

            <fieldset className="fieldset">
              <legend className="fieldset-legend border-b-2 w-18 pl-1 text-xl">意味</legend>
              <p className="text-3xl p-2">{data.meaning}</p>
            </fieldset>

            <fieldset className="fieldset">
              <legend className="fieldset-legend border-b-2 w-18 pl-1 text-xl">例文</legend>
              <p className="text-2xl p-2">{data.exampleSentence}</p>
            </fieldset>

            <fieldset className="fieldset">
              <legend className="fieldset-legend border-b-2 pl-1 text-xl">例文（日本語訳）</legend>
              <p className="text-2xl p-2">{data.exampleSentenceTranslation}</p>
            </fieldset>
          </>
        )}

        {/* エラーやデータなしの場合の簡易表示 */}
        {!isLoading && !data && wordId && (
          <p className="text-error">データの取得に失敗しました。</p>
        )}

        <div className="modal-action flex justify-between">
          <button className="btn btn-error min-w-[82px]" onClick={handleDeleteClick}>
            {isDeleting ? (
              <span className="loading loading-spinner w-6 h-6" />
            ) : (
              <>
                <BiSolidTrash />
                削除
              </>
            )}
          </button>
          <button className="btn btn-accent" onClick={handleClose}>
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
